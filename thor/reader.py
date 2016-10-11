#!/usr/bin/env python3

import datetime
from math import floor
# Import netCDF
import netCDF4


class Reader():

    def __init__(self, filename):
        # Open netCDF file for reading
        self.netCDF = netCDF4.Dataset(filename, 'r')
        self.filename = filename

        self.startLong = self.netCDF["lon"][0]
        self.startLat = self.netCDF["lat"][0]
        self.longitudeRes = abs(self.netCDF.variables['lon'][1] -
                                self.netCDF.variables['lon'][0])
        self.latitudeRes = abs(self.netCDF.variables['lat'][1] -
                               self.netCDF.variables['lat'][0])

        self.baseDate = datetime.datetime.strptime(
                self.netCDF.variables["time"].getncattr(
                    "units").split()[-1], "%Y-%m-%d"
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

    def getLongLimits(self):
        return [self.startLong, self.startLong +
                self.longitudeRes*len(self.netCDF.variables['lon'])]

    def getSurfaceTemp(self,
                       fromLong,
                       toLong,
                       fromLat,
                       toLat,
                       fromDate,
                       toDate):
        startLong = floor((fromLong-self.startLong)/self.longitudeRes)
        stopLong = floor((toLong-self.startLong)/self.longitudeRes)

        startLat = floor((fromLat-self.startLat)/self.latitudeRes)
        stopLat = floor((toLat-self.startLat)/self.latitudeRes)

        startTime = (fromDate-self.startDate).days
        stopTime = (toDate-self.startDate).days

        return self.netCDF.variables['ta'][
                startLong:stopLong,
                0,
                startLat:stopLat,
                startTime:stopTime]
