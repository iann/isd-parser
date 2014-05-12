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
db = client.stations
stationResults = db.stations

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



def parseLatLong(reading):
    if checkForNone(reading) is None:
        return None

    if len(reading) == 0:
        return 0.0

    r = float(reading)

    r = r / 1000
    if r > 180 or r < -180:
        return None
    return r


def loadLocations(csvfile):
    with open(csvfile, "r") as f:
        reader = csv.reader(f)
        i = 0
        for row in reader:
            if i != 0:
                stationId = row[0] + "-" + row[1]
                lon = parseLatLong(row[8])
                lat = parseLatLong(row[7])
                station = {}
                station["usaf"] = row[0]
                station["wban"] = row[1]
                station["stationName"] = row[2]
                station["stationId"] = stationId
                station["country"] = row[3]
                station["fipsCountry"] = row[4]
                station["state"] = row[5]
                station["callSign"] = row[6]
                if lon != "" and lat != "" and lon != None and lat != None:
                    station["loc"] = { "type": "Point", "coordinates": [lon, lat]}
                station["elevation"] = convertMeasurement(row[9])

                try:
                    stationResults.insert(station)
                except:
                    print "Insert failed, skipping" + stationId
            i += 1


def main():
    if len(sys.argv) < 2:
        print "Please run code with argument of file to be counted."
        quit()
    locFile = sys.argv[1]
    loadLocations(locFile)


if __name__ == "__main__":
    main() # will call the "main" function only when you execute this from the command line.
