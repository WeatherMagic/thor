#!/usr/bin/env python3

import thor.reader as reader
from datetime import datetime
from datetime import timedelta
import logging

def handleRequest(arguments, ncFiles, log):
    
    if "month" not in arguments:
        return {"ok": False,
                "error": "Interpolation method not implemented yet!"}
    if arguments["zoom-level"] != 1:
        return {"ok": False,
                "error": "Only zoom-level 1 implemented as of now!"}

    # This info is supplied by client
    zoomLevel = int(arguments["zoom-level"])
    startDate = datetime.strptime(arguments["year"] +
                                  arguments["month"] +
                                  "00"
                                  , "%Y%m%d")
    lastDate = startDate + timedelta(days=10)
    startLong = arguments["longitude"]
    startLat = arguments["latitude"]
    

    for ncFile in ncFiles:
        if startDate > ncFile.getStartDate() and lastDate < ncFile.getLastDate():
            pass
            
        

