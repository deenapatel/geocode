import os, subprocess, re
import pandas as pd

 # path to geosupport files and executables
path = '/home/deena/geosupport/version-20d_20.4/'

def geosupport(boro, houseNo, street,function = '1A', tpad='n', extend=''):
    '''
    Python wrapper for DCP's GeoSupport Desktop Edition.
    Before using this, download the Linux version from DCP's website: 
    http://www1.nyc.gov/site/planning/data-maps/open-data/dwn-gde-home.page
    And point 'path' variable to where the downloaded files live.
    
    More information on using GeoSupport can be found in their user guide
    GeoSupport User Guide: http://www1.nyc.gov/assets/planning/download/pdf/data-maps/open-data/upg.pdf
    
    input:  boro is the borough code, integer 1-5:
                1 (Manhattan), 2 (Bronx), 3 (Brooklyn), 4 (Queens), 5 (Staten Island)
            
            houseNO is the address house number
            
            street is the address street name
            
            function is one of the GeoSupport functions that takes address or non-addressable
            place name as input. (see GeoSuport User Guide for more info) 
            function = 1A, 1, 1E (1A is the default)
            
            tpad: y if you want TPAD data, n otherwise (see GeoSupport User Guide)
            
            extend: y if you want Extended Work Area (see GeoSupport User Guide)
    
    returns output from GeoSupport
    '''

    # set environment variables
    my_env = os.environ.copy()
    my_env["LD_LIBRARY_PATH"] = path+'lib'
    my_env["GEOFILES"] = path+'fls/'

    # path to geosupport executable
    geosupport = path+'bin/c_client'

    # open subprocess to run geosupport
    p = subprocess.Popen([geosupport],
                         env=my_env, 
                         stdout=subprocess.PIPE,
                         stdin=subprocess.PIPE,
                         stderr=subprocess.PIPE)

    
    exit = 'x'
    
    inputstring = '{}\n{}\n{}\n{}\n{}\n{}\n{}\n'.format(function,
                                                        boro,
                                                        houseNo,
                                                        street,
                                                        tpad,
                                                        extend,
                                                        exit).encode('utf-8')
    # read in input data
    stdout_data = p.communicate(input=inputstring)

    # output
    return stdout_data[0].splitlines(True)[14:]


def geosupportBatch(df,boro='boro',houseNo='houseNo',street='street'):
    ''' 
    Python wrapper for DCP's GeoSupport Desktop Edition.
    Before using this, download the Linux version from DCP's website: 
    http://www1.nyc.gov/site/planning/data-maps/open-data/dwn-gde-home.page
    And point 'path' variable to where the downloaded files live.
    
    Batch processing using GeoSupport function 1A, and returning BBL and BIN
    
    input:  dataframe df, with column names containing information on 
            the borough (boro = 1-5), 
            address house number (houseNo),
            and address street name (street).
    
    returned dataframe will have two additional columns: geocodedBBL and geocodedBIN.
    '''

    # set environment variables
    my_env = os.environ.copy()
    my_env["LD_LIBRARY_PATH"] = path+'lib'
    my_env["GEOFILES"] = path+'fls/'

    # path to geosupport executable
    expath = path+'bin/c_client'

    def hitGeoS(df):
        # open subprocess to run geosupport
        p = subprocess.Popen([expath],
                             env=my_env, 
                             stdout=subprocess.PIPE,
                             stdin=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        
        # this works with function 1A which takes address or non-addressable place name
        # as input and returns property related data including BIN, BBL
        inputstring = '{}\n{}\n{}\n{}\n{}\n{}\n{}\n'.format('1A',
                                                            df[boro],
                                                            df[houseNo],
                                                            df[street],
                                                            '','','x').encode('utf-8')
        try:
            # read input data to geosupport
            stdout_data = p.communicate(input=inputstring)
            # search for BBL data in output
            m = re.search('\[  6\]: Bbl .+[\n]',stdout_data[0])
            BBL = int(m.group()[-11:-1])
            # search for BIN data in output
            m = re.search('Bin Of Input Address .+[\n]',stdout_data[0])
            BIN = int(m.group()[-8:-1])
        except:
            m = re.search('Error Message .+[\n]',stdout_data[0])
            BBL = m.group()
            BIN = m.group()

        return BBL,BIN
    
    df[['geocodedBBL','geocodedBIN']] = df.apply(hitGeoS,axis=1).apply(pd.Series)
    return df
    