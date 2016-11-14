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

        # Creares a euclidian grid from the 3 coordinate axels
        grid = (timeCoord1D,
                latCoord1D,
                longCoord1D)

        # From the climateData and coordinate axels to the data
        # RegularGridInterpolator creates an interpolation function.
        # The interpolation function outputs interpolation value for
        # a given 3D point in the grid set.
        weatherInterpolationFunc = scipy.interpolate.RegularGridInterpolator(
            grid,
            climateData)

        # Create axis (area) where we want interpolated data returned
        interTimeCoord = np.linspace(0, maxTime-1, returnDimension[0])
        interLatCoord = np.linspace(0, maxLat-1, returnDimension[1])
        interLongCoord = np.linspace(0, maxLong-1, returnDimension[2])

        # Points (3D) created from a meshgrid of the
        # interpolation coordinate axis
        # (https://se.mathworks.com/help/matlab/ref/meshgrid.html).
        # These points are wihin the area specified in former step.
        interPoints = np.vstack(np.meshgrid(
            interTimeCoord,
            interLatCoord,
            interLongCoord,
            indexing='ij')).reshape(3, -1).T

        # Interpolate data for the 3D points created earlier
        interpolatedClimateData = (weatherInterpolationFunc(
            interPoints)).reshape(returnDimension)

        # Check so that the corners in interpolatedData and
        # climateData are the same.
        eps = 0.1
        coornerAxis = [0, -1]
        cornerPoints = np.vstack(np.meshgrid(
            coornerAxis,
            coornerAxis,
            coornerAxis)).reshape(3, -1).T

        for corner in cornerPoints:
            if(abs(interpolatedClimateData[corner[0],
                                           corner[1],
                                           corner[2]] -
                   climateData[corner[0],
                               corner[1],
                               corner[2]]) > eps):
                return {"ok": False,
                        "error":
                        "Interpolated corner data not the\
same as regular data! This is bad!"}

        return({"ok": True,
                "data": interpolatedClimateData})

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

        returnDataDict = self.interpolate(weatherData3D,
                                          stopTime-startTime,
                                          stopLat-startLat,
                                          stopLong-startLong,
                                          returnDimension)

        if not returnDataDict["ok"]:
            return None

        return (returnDataDict["data"]).tolist()
