#!/usr/bin/env python3

import thor.reader as reader
from datetime import datetime
from datetime import timedelta
import logging


def handleRequest(arguments, ncFiles, log):
    if "month" not in arguments:
        return {"ok": False,
                "error": "Interpolation method not implemented yet!"}
    if int(arguments["zoom-level"]) != 1:
        return {"ok": False,
                "error": "Only zoom-level 1 implemented as of now!"}

    # This info is supplied by client
    zoomLevel = int(arguments["zoom-level"])
    startDate = datetime.strptime(str(arguments["year"]) +
                                  str(arguments["month"]) +
                                  "1",
                                  "%Y%m%d")
    lastDate = startDate + timedelta(days=90)
    startLong = float(arguments["fromLongitude"])
    startLat = float(arguments["fromLatitude"])
    lastLat = float(arguments["toLatitude"])
    lastLong = float(arguments["toLongitude"])

    for ncFile in ncFiles:
        # Make sure data is within range
        # TODO: Enable fetching data from multiple files
        # if range is split between two files
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
