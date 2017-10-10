# NYC Geocoders
Accessing the NYC geocoders via Python.

**geosupport.py** contains two functions (single address lookup and batch lookup) for interfacing with DCP's desktop GeoSupport. Before using them, you'll need to:

1. download the __Linux version__ from [DCP's website](http://www1.nyc.gov/site/planning/data-maps/open-data/dwn-gde-home.page)
2. point the 'path' variable to where the downloaded files live on your computer.
Note: You'll need to be running linux to use this. I use [Ubuntu](https://www.ubuntu.com/download) running as a VM via [VirtualBox](https://www.virtualbox.org/wiki/Downloads) hosted on my Windows desktop.

**geoclient.py** contains a function which uses the [python wrapper](https://github.com/talos/nyc-geoclient) for the GeoClient API to geocode all addresses in a pandas dataframe. The [GeoClient API is maintained by DoITT](https://developer.cityofnewyork.us/api/geoclient-api). You should register for your own API key before using it.

**NYCgeocode.ipynb** has examples of using these functions.

Which one should you use? GeoClient is easier to use and there is no need to download software. However, if you need to geocode a ton of addresses GeoClient will be slow. In that case it's probably better to download DCP's desktop GeoSupport and run it locally on your own server. DCP updates GeoSupport every few months, so make sure you have the latest version.


If you've never used GeoSupport, DCP hosts an online tool (Geographic Online Address Translator [GOAT)](http://a030-goat.nyc.gov/goat/Default.aspx) which contains all the functions in GeoSupport, but has an easy web interface to allow  you to input addresses (or BBLs or BINs) one at a time. Also, look at their [User Guide](https://nycplanning.github.io/Geosupport-UPG/). It's very extensive.

Another useful online tool for one-off lookups is [NYCityMap](http://maps.nyc.gov/doitt/nycitymap/) maintained by DOITT.