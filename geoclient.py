from nyc_geoclient import Geoclient
import warnings, sys
import pandas as pd

def geoclientBatch(df,houseNo='houseNo',street='street',boro='boro'):
    '''
    Uses DOITT's GeoClient (the web API to DCP's GeoSupport)     
    via the python wrapper https://github.com/talos/nyc-geoclient
    to geocode a dataframe df with columns number, street, and boro.
    
    Returns the dataframe df with two additional columns: geocodedBBL and geocodedBIN
    '''
    geoID = 'fb9ad04a'
    geoKey = '051f93e4125df4bae4f7c57517e62344'
    g = Geoclient(geoID,geoKey)
    warnings.filterwarnings('ignore') #do not display warnings
    
    def hitGeoC(df):
        try:
            x = g.address(df[houseNo],df[street],df[boro])
            BBL = x['bbl']
            BIN = x['buildingIdentificationNumber']
        except:
            e = sys.exc_info()[0]
            BBL = ( "Error: %s" % e )
            BIN = BBL
        return BBL,BIN
    
    df[['geocodedBBL','geocodedBIN']] = df.apply(hitGeoC,axis=1).apply(pd.Series)
    return df
