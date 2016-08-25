# NYC Geocoders

Accessing the NYC geocoders via Python.

**geosupport.py** contains two functions for interfacing with DCP's desktop GeoSupport. Before using them, you'll need to 
1. download the Linux version from DCP's website: http://www1.nyc.gov/site/planning/data-maps/open-data/dwn-gde-home.page and 
2. point the 'path' variable to where the downloaded files live on your computer.

**geoclient.py** contains a function which uses the python wrapper for the GeoClient API (https://github.com/talos/nyc-geoclient) to geocode all addresses in a pandas dataframe. The GeoClient API is maintained by DoITT (https://developer.cityofnewyork.us/api/geoclient-api). You should register for your own API key before using it.


Which one should you use? GeoClient is easier to use and there is no need to download software. However, if you need to geocode a ton of addresses GeoClient will be slow and so it's probably better to download DCP's desktop GeoSupport and run it locally on your own server. DCP updates GeoSupport every few months, so make sure you have the latest version.


**NYCgeocode.ipynb** has examples of using these functions.