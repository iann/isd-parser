#!/usr/bin/python

import sys, datetime, csv, gzip
from os import listdir
from os.path import isfile, join

from multiprocessing import Pool

__author__ = "Ian Moriarty"


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


readings = {}
tmax = {"key": "Max Temp",
        "color": "red"}

tmin = {"key": "Min Temp",
        "color" : "blue"}

tmaxes = []
tmins = []

def loadLocations(csvfile):
    with open(csvfile, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            date = row[1]
            event = row[2]
            measurement = convertMeasurement(row[3])
            dvpair = {"x" : date[4:6] + "/" + date[6:], "y" : measurement}
            if event == "TMAX" or event == "TMIN":
                value = {event : measurement}
                if readings.has_key(date):
                    readings[date].update(value)
                else:
                    readings[date] = value

            if event == "TMAX":
                tmaxes.append(dvpair)

            if event == "TMIN":
                tmins.append(dvpair)


def main():
    if len(sys.argv) < 2:
        print "Please run code with argument of file to be counted."
        quit()
    locFile = sys.argv[1]
    loadLocations(locFile)

    tmax["values"] = tmaxes
    tmin["values"] = tmins

    result = [tmax , tmin]
    print result

if __name__ == "__main__":
    main() # will call the "main" function only when you execute this from the command line.