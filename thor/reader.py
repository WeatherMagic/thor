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


class Reader():

    """
    Takes a file path to a netcdf file and loads it.
    """
    def __init__(self, filename):
        # Open netCDF file for reading
        self.netCDF = netCDF4.Dataset(filename, 'r')
        self.filename = filename

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
        dateString = dateString[0:6] + "01"

        self.baseDate = datetime.datetime.strptime(
                dateString,
                "%Y%m%d"
                )

        self.startDate = \
            self.baseDate + \
            datetime.timedelta(
                days=self.netCDF["time"][0]
            )
        self.startDate = datetime.datetime(
                self.startDate.year,
                self.startDate.month,
                1
                )

        last = len(self.netCDF.variables['time']) - 1
        lastDate = self.baseDate +\
            datetime.timedelta(days=self.netCDF.variables['time'][last])
        self.lastDate = datetime.datetime(lastDate.year, lastDate.month, 1)

        # Avg nr of days / month
        self.dateResolution = 30.42

        if "i" in self.domain:
            self.minLat = self.netCDF.variables['lat'][0]
            self.maxLat = self.netCDF.variables['lat'][-1]
            self.minLon = self.netCDF.variables['lon'][0]
            self.maxLon = self.netCDF.variables['lon'][-1]
            self.lonLen = len(self.netCDF["lon"])
            self.latLen = len(self.netCDF["lat"])
            self.latScale = self.latLen / (self.maxLat-self.minLat)
            self.lonScale = self.lonLen / (self.maxLon-self.minLon)
        else:
            self.lonLen = len(self.netCDF["rlon"])-1
            self.latLen = len(self.netCDF["rlat"])-1

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
        return self.lastDate

    """
     Finds overlaping area between file area and
     area requested of Thor.
    """
    def overlap(self,
                fromLat,
                toLat,
                fromLong,
                toLong):

        # Checking overlap
        if self.minLat > toLat:
            return {"ok": False,
                    "error": "No overlap"}
        if self.maxLat < fromLat:
            return {"ok": False,
                    "error": "No overlap"}
        if self.minLon > toLong:
            return {"ok": False,
                    "error": "No overlap"}
        if self.maxLon < fromLong:
            return {"ok": False,
                    "error": "No overlap"}

        # Checking overlaping area between
        # requesting area and this file
        # If overlap only take out the
        # data that is within the overlap
        if self.minLat > fromLat:
            fromLat = self.minLat
        if self.maxLat < toLat:
            toLat = self.maxLat
        if self.minLon > fromLong:
            fromLong = self.minLon
        if self.maxLon < toLong:
            toLong = self.maxLon

        return {"ok": True,
                "area": [fromLat,
                         toLat,
                         fromLong,
                         toLong]}

    """
    Gets indexes for a given area from within the file
    """
    def getArea(self,
                fromDate,
                toDate,
                fromLat,
                toLat,
                fromLong,
                toLong):

        startTime = int(round((fromDate-self.startDate).days /
                              self.dateResolution))
        stopTime = startTime + 1

        # Due to how numpy range-indexing works, we need one more.
        # if stopTime < len(self.netCDF.variables["time"]) - 1:

        startLat = int(floor((fromLat - self.minLat) * self.latScale))
        stopLat = int(floor((toLat - self.minLat) * self.latScale))
        startLong = int(floor((fromLong - self.minLon) * self.lonScale))
        stopLong = int(floor((toLong - self.minLon) * self.lonScale))

        return({"ok": True,
                "data": [startTime,
                         stopTime,
                         startLat,
                         stopLat,
                         startLong,
                         stopLong]})
    """
    Returns data in an area of an netcdf file.
    The area is determined by checking overlap
    between requested area and area in file.
    """
    def getData(self,
                fromDate,
                toDate,
                fromLat,
                toLat,
                fromLong,
                toLong):

        overlapDict = self.overlap(fromLat,
                                   toLat,
                                   fromLong,
                                   toLong)

        if not overlapDict["ok"]:
            return overlapDict

        [fromLat,
         toLat,
         fromLong,
         toLong] = overlapDict["area"]

        areaDict = self.getArea(fromDate,
                                toDate,
                                fromLat,
                                toLat,
                                fromLong,
                                toLong)

        if not areaDict["ok"]:
            return areaDict

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
                    "error":
                    "Specified area did not contain any data"}

        return {"ok": True,
                "data":
                weatherData3D,
                "area": [fromLat,
                         toLat,
                         fromLong,
                         toLong]}
