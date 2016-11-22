#!/usr/bin/env python3

import datetime
from math import floor
from math import ceil
import numpy as np
import scipy.interpolate
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

        self.lonLen = len(self.netCDF["rlon"])-1
        self.latLen = len(self.netCDF["rlat"])-1

        # Getting meta data from the netCDF file
        for key in self.netCDF.variables.keys():
            if key in filename:
                self.variable = key
                break

        metaData = str(self.netCDF)

        for line in metaData.split("\n"):
            temp = line.split(": ")
            if len(temp) > 1:
                key = temp[0]
                value = temp[1]
                if "experiment" in key:
                    self.experiment = value
                elif "driving_model_id" in key:
                    self.model = value
                elif "CORDEX_domain" in key:
                    self.domain = value

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

    # -------------------------------------
    def getVariable(self):
        return self.variable

    # -------------------------------------
    def getExperiment(self):
        return self.experiment

    # -------------------------------------
    def getModel(self):
        return self.model

    # -------------------------------------
    def getDomain(self):
        return self.domain

    # -------------------------------------
    def getDimensionData(self, dimension):
        return self.netCDF.variables[dimension]

    # -------------------------------------
    def getFileName(self):
        return self.filename

    # -------------------------------------
    def getStartDate(self):
        return self.startDate

    # -------------------------------------
    def getLastDate(self):
        last = len(self.netCDF.variables['time']) - 1
        return self.baseDate +\
            datetime.timedelta(days=self.netCDF.variables['time'][last])

    # -------------------------------------
    def getArea(self,
                fromDate,
                toDate,
                fromLat,
                toLat,
                fromLong,
                toLong):

        startTime = int(round((fromDate-self.startDate).days /
                              self.dateResolution))
        stopTime = int(round((toDate-self.startDate).days /
                             self.dateResolution))
        # Due to how numpy range-indexing works, we need one more.
        if stopTime < len(self.netCDF.variables["time"]) - 1:
            stopTime = stopTime + 1

        # Find where to start and stop in rotated coordinates
        rotFrom = transform.toRot(fromLat, fromLong)
        rotTo = transform.toRot(toLat, toLong)

        startLat = 0
        while self.netCDF.variables['rlat'][
                startLat] < rotFrom.item(1, 0):
            if startLat < self.latLen:
                startLat = startLat + 1
            else:
                return {"ok": False}

        stopLat = startLat
        while self.netCDF.variables['rlat'][stopLat] < rotTo.item(1, 0):
            if stopLat < self.latLen:
                stopLat = stopLat + 1
            else:
                return {"ok": False}

        startLong = 0
        while self.netCDF.variables['rlon'][
                startLong] < rotFrom.item(0, 0):
            if startLong < self.lonLen:
                startLong = startLong + 1
            else:
                return {"ok": False}

        stopLong = startLong + 1
        while self.netCDF.variables['rlon'][
              stopLong] < rotTo.item(0, 0):
            if stopLong < self.lonLen:
                stopLong = stopLong + 1
            else:
                return {"ok": False}

        return({"ok": True,
                "data": [startTime,
                         stopTime,
                         startLat,
                         stopLat,
                         startLong,
                         stopLong]})

    # -------------------------------------
    def getData(self,
                fromDate,
                toDate,
                fromLat,
                toLat,
                fromLong,
                toLong):

        areaDict = self.getArea(fromDate,
                                toDate,
                                fromLat,
                                toLat,
                                fromLong,
                                toLong)

        if not areaDict["ok"]:
            return {"ok": False,
                    "errorMessage":
                    "Specified lat/lon combination not" +
                    " within server dataset."}

        [startTime,
         stopTime,
         startLat,
         stopLat,
         startLong,
         stopLong] = areaDict["data"]

        weatherData3D = self.netCDF.variables[self.variable][
            startTime:stopTime,
            startLat:stopLat,
            startLong:stopLong]

        if not weatherData3D.size:
            return {"ok": False,
                    "errorMessage":
                    "Specified area did not contain any data"}

        return {"ok": True,
                "data":
                weatherData3D}
