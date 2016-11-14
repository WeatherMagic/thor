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
    def interpolate(self,
                    climateData,
                    maxTime,
                    maxLat,
                    maxLong,
                    returnDimension):

        # Coordinates to the climateData
        timeCoord1D = np.linspace(0, maxTime-1, maxTime)
        latCoord1D = np.linspace(0, maxLat-1, maxLat)
        longCoord1D = np.linspace(0, maxLong-1, maxLong)

        grid = (timeCoord1D,
                latCoord1D,
                longCoord1D)

        # Creates an interpolation function that can return any
        # interpolated value to any 3D-point the climateData
        weatherInterpolationFunc = scipy.interpolate.RegularGridInterpolator(
            grid,
            climateData)

        # Interpolation coordinates
        interTimeCoord1D = np.linspace(0, maxTime-1, returnDimension[0])
        interLatCoord1D = np.linspace(0, maxLat-1, returnDimension[1])
        interLongCoord1D = np.linspace(0, maxLong-1, returnDimension[2])

        # Interpolation 3D points
        interPoints = np.vstack(np.meshgrid(
            interTimeCoord1D,
            interLatCoord1D,
            interLongCoord1D)).reshape(3, -1).T

        # Interpolation from the interpolation 3D points
        returnData3D = (weatherInterpolationFunc(
            interPoints)).reshape(returnDimension)

        return returnData3D

    # -------------------------------------
    def getSurfaceTemp(self,
                       fromDate,
                       toDate,
                       fromLat,
                       toLat,
                       fromLong,
                       toLong,
                       returnDimension):
        areaDict = self.getArea(fromDate,
                                toDate,
                                fromLat,
                                toLat,
                                fromLong,
                                toLong)
        if not areaDict["ok"]:
            return None

        [startTime,
         stopTime,
         startLat,
         stopLat,
         startLong,
         stopLong] = areaDict["data"]

        weatherData3D = self.netCDF.variables['tas'][startTime:stopTime,
                                                     startLat:stopLat,
                                                     startLong:stopLong]

        returnData3D = self.interpolate(weatherData3D,
                                        stopTime-startTime,
                                        stopLat-startLat,
                                        stopLong-startLong,
                                        returnDimension)

        return returnData3D.tolist()
