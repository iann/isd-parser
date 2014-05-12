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
        f = r / 10
        c = (f - 32.0) * (5.0/9.0)
        return round(c,1)



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
jan = {"key": "Jan.",
        "color": "#FFD12A",
        "values": []}

feb = {"key": "Feb.",
        "color" : "#DA2647",
        "values": []}

mar = {"key": "Mar.",
       "color" : "#DB91EF",
       "values": []}

apr = {"key": "Apr.",
       "color" : "#214FC6",
       "values": []}

may = {"key": "May",
       "color" : "#6F2DA8",
       "values": []}

june = {"key": "June",
       "color" : "#C95A49",
       "values": []}

july = {"key": "July",
       "color" : "#4F86F7",
       "values": []}

aug = {"key": "Aug.",
       "color" : "#45A27D",
       "values": []}

sept = {"key": "Sept.",
       "color" : "#B2F302",
       "values": []}

oct = {"key": "Oct.",
       "color" : "#CEC8EF",
       "values": []}

nov = {"key": "Nov.",
       "color" : "#44D7A8",
       "values": []}

dec = {"key": "Dec.",
       "color" : "#FFD3F8",
       "values": []}


def loadLocations(csvfile):
    with open(csvfile, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            date = row[2]
            month = row[2][4:]
            measurement = convertMeasurement(row[3])
            dvpair = {"x" :  date[4:]+ "/" + date[0:4], "y" : measurement}

            if month == "01":
                jan["values"].append(dvpair)
            elif month == "02":
                feb["values"].append(dvpair)
            elif month == "03":
                mar["values"].append(dvpair)
            elif month == "04":
                apr["values"].append(dvpair)
            elif month == "05":
                may["values"].append(dvpair)
            elif month == "06":
                june["values"].append(dvpair)
            elif month == "07":
                july["values"].append(dvpair)
            elif month == "08":
                aug["values"].append(dvpair)
            elif month == "09":
                sept["values"].append(dvpair)
            elif month == "10":
                oct["values"].append(dvpair)
            elif month == "11":
                nov["values"].append(dvpair)
            elif month == "12":
                dec["values"].append(dvpair)


def main():
    if len(sys.argv) < 2:
        print "Please run code with argument of file to be counted."
        quit()
    locFile = sys.argv[1]
    loadLocations(locFile)

    result = [jan,
              feb,
              mar,
              apr,
              may,
              june,
              july,
              aug,
              sept,
              oct,
              nov,
              dec]

    print result

if __name__ == "__main__":
    main() # will call the "main" function only when you execute this from the command line.