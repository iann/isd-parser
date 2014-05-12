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

`python station-loader.py ish-history.csv`

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
