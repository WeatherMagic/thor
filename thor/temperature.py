#!/usr/bin/env python3

import thor.reader as reader
from datetime import datetime
from datetime import timedelta
import logging


def handleRequest(arguments, ncFiles, log):
    if "month" not in arguments:
        return {"ok": False,
                "error": "Interpolation method not implemented yet!"}
    if arguments["zoom-level"] != "1":
        return {"ok": False,
                "error": "Only zoom-level 1 implemented as of now!"}

    # This info is supplied by client
    zoomLevel = int(arguments["zoom-level"])
    startDate = datetime.strptime(arguments["year"] +
                                  arguments["month"] +
                                  "1",
                                  "%Y%m%d")
    lastDate = startDate + timedelta(days=10)
    startLong = int(arguments["longitude"])
    startLat = int(arguments["latitude"])
    lastLong = startLong + 10
    lastLat = startLat + 10
    
    for ncFile in ncFiles:
        print("")
        print("startLong: " + str(ncFile.getStartLong()))
        print("stopLong: " + str(ncFile.getLastLong()))
        print("startLat: " + str(ncFile.getStartLat()))
        print("stopLat: " + str(ncFile.getLastLat()))
        if startDate > ncFile.getStartDate()\
                and lastDate < ncFile.getLastDate()\
                and startLong > ncFile.getStartLong()\
                and lastLong < ncFile.getLastLong()\
                and startLat > ncFile.getStartLong()\
                and lastLat < ncFile.getLastLat():
                    returnData = {"ok": True,
                                  "data": ncFile.getSurfaceTemp(startLong,
                                                                lastLong,
                                                                startLat,
                                                                lastLat,
                                                                startDate,
                                                                lastDate)}
                    return returnData

    returnData = {"ok": False,
                  "errorMessage":
                   "Specified range not within server dataset."}
    return returnData
