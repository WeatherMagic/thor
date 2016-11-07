#!/usr/bin/env python3

import datetime
from math import floor
from math import ceil
# Import netCDF
import netCDF4
# Regex
import re
import thor.transform as transform


class Reader():

    def __init__(self, filename):
        # Open netCDF file for reading
        self.netCDF = netCDF4.Dataset(filename, 'r')
        self.filename = filename

        # Last lonLat, the file seems to start backwards?
        lonLat = transform.regFromRot(
                self.netCDF["rlon"][0],
                self.netCDF["rlat"][0])
        self.lastLong = lonLat.item(0, 0)
        self.lastLat = lonLat.item(1, 0)
        # start lonLat
        lonLen = len(self.netCDF["rlon"])-1
        latLen = len(self.netCDF["rlat"])-1
        lonLat = transform.regFromRot(
                self.netCDF["rlon"][lonLen],
                self.netCDF["rlat"][latLen])
        self.startLong = lonLat.item(0, 0)
        self.startLat = lonLat.item(1, 0)

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
        dateString = dateString[0:8]

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
        return self.baseDate +\
            datetime.timedelta(days=self.netCDF.variables['time'][last])

    def getStartLong(self):
        return self.startLong

    def getLastLong(self):
        return self.lastLong

    def getStartLat(self):
        return self.startLat

    def getLastLat(self):
        return self.lastLat

    def getArea(self,
                fromLong,
                toLong,
                fromLat,
                toLat,
                fromDate,
                toDate):

        # Find where to start and stop in rotated coordinates
        rotFrom = transform.rotFromReg(fromLong, fromLat)
        rotTo = transform.rotFromReg(toLong, toLat)

        startLong = len(self.netCDF.variables['rlon']) - 1
        while self.netCDF.variables['rlon'][startLong] > rotFrom[0]:
            startLong = startLong - 1

        stopLong = startLong - 1
        while self.netCDF.variables['rlon'][stopLong] > rotTo[0]:
            stopLong = stopLong - 1

        startLat = len(self.netCDF.variables['rlat']) - 1
        while self.netCDF.variables['rlat'][startLat] > rotFrom[1]:
            startLat = startLat - 1

        stopLat = startLat
        while self.netCDF.variables['rlat'][stopLat] > rotTo[1]:
            stopLat = stopLat - 1

        startTime = floor((fromDate-self.startDate).days/self.dateResolution)
        stopTime = ceil((toDate-self.startDate).days/self.dateResolution)

        return(startLong,
               stopLong,
               startLat,
               stopLat,
               startTime,
               stopTime)

    def getSurfaceTemp(self,
                       fromLong,
                       toLong,
                       fromLat,
                       toLat,
                       fromDate,
                       toDate,
                       zoomLevel):
        [startLong,
         stopLong,
         startLat,
         stopLat,
         startTime,
         stopTime] = self.getArea(fromLong,
                                  toLong,
                                  fromLat,
                                  toLat,
                                  fromDate,
                                  toDate)

        returnData = self.netCDF.variables['tas'][startTime:stopTime,
                                                  stopLat:startLat:zoomLevel,
                                                  stopLong:startLong:zoomLevel]

        return returnData.tolist()

    def getSurfacePersp(self,
                        fromLong,
                        toLong,
                        fromLat,
                        toLat,
                        fromDate,
                        toDate,
                        zoomLevel):
        [startLong,
         stopLong,
         startLat,
         stopLat,
         startTime,
         stopTime] = self.getArea(fromLong,
                                  toLong,
                                  fromLat,
                                  toLat,
                                  fromDate,
                                  toDate)

        returnData = self.netCDF.variables['pr'][startTime:stopTime,
                                                 stopLat:startLat:zoomLevel,
                                                 stopLong:startLong:zoomLevel]

        return returnData.tolist()
