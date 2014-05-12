# ISD-Parser and Other Scripts
Code to parse NOAA ISD-Lite dataset and insert into a MongoDB

## Setup

* Download NOAA's ISD-Lite Dataset (ftp://ftp3.ncdc.noaa.gov/pub/data/noaa/isd-lite/)

While you're waiting...

* Download and Install MongoDB (http://www.mongodb.org/downloads)

## Running

This example assumes that the loader scripts run the same machine as the database.
If not edit line 14 of `data-loader.py` and `station-loader.py`

### Load Stations

`$ python station-loader.py ish-history.csv`

This command will create a new collection in your MongoDB called stations.
Stations contains a document for each station. Example below.

```
{
  "_id" : ObjectId("536ee8ebba328ccfb195c664"),
  "loc" : {
    "type" : "Point",
    "coordinates" : [
      -71.011,
      42.361
    ]
  },
  "elevation" : 9.1,
  "wban" : "14739",
  "state" : "MA",
  "country" : "US",
  "usaf" : "725090",
  "stationId" : "725090-14739",
  "callSign" : "KBOS",
  "fipsCountry" : "US",
  "stationName" : "BOSTON/LOGAN INTL"
}
```

### Load Weather

`data-loader.py` takes in ish-history.csv and a folder containing compressed weather data as paramaters.

`data-loader.py` is a multiprocess python application in order to change the number of pooled processes edit line 202.
Default = 6

`pool = Pool(processes=6)`


To run on the attached 1901 ISD data one would use.

`$ python data-loader.py ish-history.csv data/1901`

#### Batch Load Weather

Use `scripts/batch-command.sh`.
