#!/usr/bin/env python3

import datetime
from math import floor
# Import netCDF
import netCDF4
# Regex
import re


class Reader():

    def __init__(self, filename):
        # Open netCDF file for reading
        self.netCDF = netCDF4.Dataset(filename, 'r')
        self.filename = filename

        self.startLong = self.netCDF["lon"][0][0]
        self.startLat = self.netCDF["lat"][0][0]

        # NetCDF file contains a date string looking like:
        # days since YYYY-MM-DD HH:MM:SS
        # or
        # days since YYYY-MM-DD
        #
        # We only want "YYYY-MM-DD", make sure we get it
        dateString = self.netCDF.variables["time"].getncattr("units")
        # Replace all non-digit characters
        dateString = re.sub("\D", "", dateString)
        # Get only first 8 digits
        dateString = dateString[0:7]

        self.baseDate = datetime.datetime.strptime(
                dateString,
                "%Y%m%d"
                )

        self.startDate = \
            self.baseDate + \
            datetime.timedelta(
                days=self.netCDF["time"][0]
            )

        self.dateResolution = abs(self.netCDF.variables['time'][1] -
                                  self.netCDF.variables['time'][0])

    def getDimensionData(self, dimension):
        return self.netCDF.variables[dimension]

    def getFileName(self):
        return self.filename

    def getStartDate(self):
        return self.startDate

    def getLastDate(self):
        last = len(self.netCDF.variables['time']) - 1
        return self.startDate +\
            datetime.timedelta(days=self.netCDF.variables['time'][last])

    def getStartLong(self):
        return self.startLong

    def getLastLong(self):
        return self.longitudeRes*len(self.netCDF.variables['lon'])

    def getStartLat(self):
        return self.startLat

    def getLastLat(self):
        return self.latitudeRes*len(self.netCDF.variables['lat'])

    def getSurfaceTemp(self,
                       fromLong,
                       toLong,
                       fromLat,
                       toLat,
                       fromDate,
                       toDate):
        
        stopLat = 0
        maxLen = len(self.netCDF.variables["rlat"])
        while True:
            if stopLat < maxLen:
                if self.netCDF.variables["lat"][stopLat][1] > toLat:
                    stopLat = stopLat + 1
                else:
                    break
            else:
                return {"ok": False, "error": "Latitiude not within file for this time period..."}

        stopLong = 0
        maxLen = len(self.netCDF.variables["rlong"])
        while True:
            if stopLong < maxLen:
                if self.netCDF.variables["long"][stopLong][1] > toLat:
                    stopLong = stopLong + 1
                    continue
                break
            else:
                return {"ok": False, "error": "Latitiude not within file for this time period..."}

        startTime = (fromDate-self.startDate).days
        stopTime = (toDate-self.startDate).days

        return self.netCDF.variables['ta'][
                startLong:stopLong,
                0,
                startLat:stopLat,
                startTime:stopTime].tolist()
