from nyc_geoclient import Geoclient
import warnings, sys
import pandas as pd
from requests.exceptions import ProxyError


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
        # try to query the Geoclient API
        try:
            x = g.address(df[houseNo], df[street], df[boro])

            # try to get BBL
            try:
                BBL = x['bbl']
            # if there is a proxy error, display "---ProxyError---"
            except ProxyError:
                BBL = '---ProxyError---'
            # if there is any other error, display "---InvalidAddress---"
            except:
                BBL = ''

            # try to get BIN
            try:
                BIN = x['buildingIdentificationNumber']
            # if there is a proxy error, display "---ProxyError---"
            except ProxyError:
                BIN = '---ProxyError---'
            # if there is any other error, display "---InvalidAddress---"
            except:
                BIN = ''

        # if there is a proxy error, display "---ProxyError---" for every value
        except ProxyError:
            error_message = '---ProxyError---'
            BBL = error_message
            BIN = error_message

        # if there is any other error, display "---InvalidAddress---" for every value
        except:
            error_message = '---InvalidAddress---'
            BBL = error_message
            BIN = error_message

        # return the geocoded columns
        return BBL,BIN

    # applies the "hitGeoC" function to every row in the DataFrame
    df[['geoBBL','geoBIN']] = df.apply(hitGeoC,axis=1).apply(pd.Series)
    
    return df
