#!/usr/bin/python

import csv, json, sys
from os import listdir
from os.path import isfile, join

from multiprocessing import Pool

__author__ = "Ian Moriarty"

locations = {}


def checkForNone(reading):
    if reading in ("-9999", "-99999", "-999999", ""):
        return None
    else:
        return False


def convertMeasurement(reading):
    if checkForNone(reading) is None:
        return None
    else:
        r = float(reading)
        return r / 10


def parseLatLong(reading):
    if checkForNone(reading) is None:
        return ""

    if len(reading) == 0:
        return 0.0

    r = float(reading)
    return r / 1000


def loadLocations(csvfile):
    with open(csvfile, "r") as f:
        reader = csv.reader(f)
        i = 0
        for row in reader:
            if i == 0:
                #print "stationId,usaf,wban,stationName,country,fipsCountry,state,callSign,lat,lon,elevation,begin,end"
                print "1,0"
            if i != 0 and str(parseLatLong(row[7])) != "" and str(parseLatLong(row[8])) != "" and row[11] != "":
                # print row[0] + "-" + row[1] + "," + row[0] + "," + row[1] + ",\"" + \
                #       row[2] + "\"," + row[3] + "," + row[4] + "," + row[5] + "," + \
                #       row[6] + "," + str(parseLatLong(row[7])) + "," + str(parseLatLong(row[8])) + "," + \
                #       str(convertMeasurement(row[9])) + "," + row[10] + "," + row[11]
                print str(parseLatLong(row[7])) + "," + str(parseLatLong(row[8]))

            i += 1


def documentReturn(station):
    return locations[station]


def main():
    if len(sys.argv) < 2:
        print "Please run code with argument of file to be counted."
        quit()
    locFile = sys.argv[1]
    loadLocations(locFile)


if __name__ == "__main__":
    main() # will call the "main" function only when you execute this from the command line.