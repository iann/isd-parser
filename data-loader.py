#!/usr/bin/python

import sys, datetime, csv, gzip
from os import listdir
from os.path import isfile, join
import pymongo
from pymongo import MongoClient

from multiprocessing import Pool

__author__ = "Ian Moriarty"

#db setup
client = MongoClient()
db = client.weather
weatherResults = db.weather

locations = {}


# loader
def loadData(file):
    stationId = file[7:-8]
    try:
        result = locations[stationId]['details']
    except:
        print "Station not found, skipping: " + stationId
        return
    i = 0
    result["stationId"] = stationId
    with gzip.open(file, "r") as txt:
        for line in txt:
            l = line.split()

            #convert to correct types etc
            year          = int(l[0])                                  # l[0] # year
            month         = int(l[1])                                  # l[1] # month
            day           = int(l[2])                                  # l[2] # day
            hour          = int(l[3])                                  # l[3] # hour

            airTemp       = convertMeasurement(l[4])             # l[4] # air temp degrees C * 10 or -9999
            dewPt         = convertMeasurement(l[5])             # l[5] # dew point degrees C * 10 or -9999
            pressure      = convertMeasurement(l[6])             # l[6] # sea level pressure hectopascals * 10 or -9999
            windDirection = convertMeasurementNoScaling(l[7])    # l[7] # wind direction angular degrees
            windSpeed     = convertMeasurement(l[8])             # l[8] # wind speed rate meters per second * 10
            cloudCover    = cloudCoverLookup(l[9])               # l[9] # MISSING VALUE: -9999
                                                                    # DOMAIN:
                                                                    # 0: None, SKC or CLR
                                                                    # 1: One okta - 1/10 or less but not zero
                                                                    # 2: Two oktas - 2/10 - 3/10, or FEW
                                                                    # 3: Three oktas - 4/10
                                                                    # 4: Four oktas - 5/10, or SCT
                                                                    # 5: Five oktas - 6/10
                                                                    # 6: Six oktas - 7/10 - 8/10
                                                                    # 7: Seven oktas - 9/10 or more but not 10/10, or BKN
                                                                    # 8: Eight oktas - 10/10, or OVC
                                                                    # 9: Sky obscured, or cloud amount cannot be estimated
                                                                    # 10: Partial obscuration
                                                                    # 11: Thin scattered
                                                                    # 12: Scattered
                                                                    # 13: Dark scattered
                                                                    # 14: Thin broken
                                                                    # 15: Broken
                                                                    # 16: Dark broken
                                                                    # 17: Thin overcast
                                                                    # 18: Overcast
                                                                    # 19: Dark overcast
            precipShortDuration = convertMeasurement(l[10])      # l[10] # The depth of liquid precipitation that is measured over a one hour accumulation period. UNITS: cm
            precipLongDuration  = convertMeasurement(l[11])      # l[11] # The depth of liquid precipitation that is measured over a six hour accumulation period. UNITS: cm


            dt = datetime.datetime(year, month, day, hour)

            reading = {
                    "timestamp": dt,
                    "airTemp": airTemp,
                    "dewPoint": dewPt,
                    "pressure": pressure,
                    "windDirection": windDirection,
                    "windSpeed": windSpeed,
                    "cloudCover": cloudCover,
                    "oneHourPrecipitation": precipShortDuration,
                    "sixHourPrecipitation": precipLongDuration
                }

            if i == 0:
                result['year'] = year
                result['observations'] = {}

            result['observations'].update({str(dt): reading})
            i += 1

    #print result
    try:
        weatherResults.insert(result)
    except:
        print "Insert failed, skipping" + stationId


def checkForNone(reading):
    if reading in ("-9999", "-99999", "-999999", ""):
        return None
    else:
        return False


def convertMeasurementNoScaling(reading):
    if checkForNone(reading) is None:
        return None
    else:
        return float(reading)


def convertMeasurement(reading):
    if checkForNone(reading) is None:
        return None
    else:
        r = float(reading)
        return r / 10


def cloudCoverLookup(reading):
    return {
        "0": "None, SKC or CLR",
        "1": "One okta - 1/10 or less but not zero",
        "2": "Two oktas - 2/10 - 3/10, or FEW",
        "3": "Three oktas - 4/10",
        "4": "Four oktas - 5/10, or SCT",
        "5": "Five oktas - 6/10",
        "6": "Six oktas - 7/10 - 8/10",
        "7": "Seven oktas - 9/10 or more but not 10/10, or BKN",
        "8": "Eight oktas - 10/10, or OVC",
        "9": "Sky obscured, or cloud amount cannot be estimated",
        "10": "Partial obscuration",
        "11": "Thin scattered",
        "12": "Scattered",
        "13": "Dark scattered",
        "14": "Thin broken",
        "15": "Broken",
        "16": "Dark broken",
        "17": "Thin overcast",
        "18": "Overcast",
        "19": "Dark overcast",
    }.get(reading)


def parseLatLong(reading):
    if checkForNone(reading) is None:
        return None

    if len(reading) == 0:
        return 0.0

    r = float(reading)
    return r / 1000


def loadLocations(csvfile):
    with open(csvfile, "r") as f:
        reader = csv.reader(f)
        i = 0
        for row in reader:
            if i != 0:
                station = row[0] + "-" + row[1]
                details = \
                    { "details":
                          {
                              "usaf": row[0],
                              "wban": row[1],
                              "stationName": row[2],
                              "country": row[3],
                              "fipsCountry": row[4],
                              "state": row[5],
                              "callSign": row[6],
                              "lat": parseLatLong(row[7]),
                              "lon": parseLatLong(row[8]),
                              "elevation": convertMeasurement(row[9])
                          }
                    }
                locations.update({station: details})
            i += 1


def documentReturn(station):
    return locations[station]


def main():
    if len(sys.argv) < 2:
        print "Please run code with argument of file to be counted."
        quit()
    locFile = sys.argv[1]
    loadLocations(locFile)

    folder = sys.argv[2]
    onlyfiles = [ join(folder,f) for f in listdir(folder) if isfile(join(folder,f)) ]
    #print onlyfiles

    #db setup

    #print locations
    pool = Pool(processes=6)
    pool.map(loadData, onlyfiles)
    #print result


if __name__ == "__main__":
    main() # will call the "main" function only when you execute this from the command line.