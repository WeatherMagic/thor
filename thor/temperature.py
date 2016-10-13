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

    for ncFile in ncFiles:
        if startDate > ncFile.getStartDate()\
                and lastDate < ncFile.getLastDate():
                    returnData = {"ok": True,
                                  "data": ncFile.getSurfaceTemp(startLong,
                                                                startLong+45,
                                                                startLat,
                                                                startLat+25,
                                                                startDate,
                                                                lastDate)}
                    return returnData
        else:
            returnData = {"ok": False,
                          "errorMessage":
                          "Specified range not within server dataset."}
            return returnData
