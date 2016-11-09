#!/usr/bin/env python3

import thor.reader as reader
from datetime import datetime
from datetime import timedelta
import logging


def handleRequest(arguments, ncFiles, log):
    if "from-month" not in arguments or "to-month" not in arguments:
        return {"ok": False,
                "error": "Interpolation method not implemented yet!"}
    if int(arguments["zoom-level"]) != 1:
        return {"ok": False,
                "error": "Only zoom-level 1 implemented as of now!"}

    # This info is supplied by client
    zoomLevel = int(arguments["zoom-level"])
    startDate = datetime.strptime(str(arguments["from-year"]) +
                                  str(arguments["from-month"]) +
                                  "1",
                                  "%Y%m%d")
    lastDate = datetime.strptime(str(arguments["to-year"]) +
                                 str(int(arguments["to-month"])) +
                                 "1",
                                 "%Y%m%d")
    startLong = float(arguments["from-longitude"])
    startLat = float(arguments["from-latitude"])
    lastLat = float(arguments["to-latitude"])
    lastLong = float(arguments["to-longitude"])

    for ncFile in ncFiles:
        # Make sure data is within range
        # TODO: Enable fetching data from multiple files
        # if range is split between two files
        if startDate > ncFile.getStartDate()\
                and lastDate < ncFile.getLastDate():
                    # If returnArea is None, it is not within file
                    returnArea = ncFile.getSurfaceTemp(startLong,
                                                       lastLong,
                                                       startLat,
                                                       lastLat,
                                                       startDate,
                                                       lastDate)
                    if returnArea is not None:
                        return {"ok": True,
                                "data": returnArea}
                    # Else lat/lon comb not in file
                    return {"ok": False,
                            "errorMessage":
                            "Specified lat/lon combination not \
within server dataset."}

    returnData = {"ok": False,
                  "errorMessage":
                  "Specified date range not within server dataset."}
    return returnData
