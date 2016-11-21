#!/usr/bin/env python3

import thor.reader as reader
from datetime import datetime
from datetime import timedelta
import numpy as np
import logging


def getList(dictTree,
            domain,
            model,
            experiment,
            variable):

    return dictTree[domain][model][experiment][variable]


def handleRequest(arguments, ncFileDictTree, log):
    if "from-month" not in arguments or "to-month" not in arguments:
        return {"ok": False,
                "error": "Interpolation method not implemented yet!"}

    # This info is supplied by client
    returnDimension = np.array(arguments["return-dimension"])
    fromDate = datetime.strptime(str(arguments["from-year"]) +
                                 str(arguments["from-month"]) +
                                 "1",
                                 "%Y%m%d")
    toDate = datetime.strptime(str(arguments["to-year"]) +
                               str(int(arguments["to-month"])) +
                               "1",
                               "%Y%m%d")
    fromLat = float(arguments["from-latitude"])
    fromLong = float(arguments["from-longitude"])

    toLat = float(arguments["to-latitude"])
    toLong = float(arguments["to-longitude"])
    dimension = arguments["dimension"]


    # ---------------
    """ TODO: Until we expose different climate models within the API
     - we just set default values for them """
    variable = arguments["dimension"]
    if "domain" not in arguments:
        domain = list(ncFileDictTree.keys())[0]
    else:
        domain = str(arguments["domain"])
    if "model" not in arguments:
        model = list(ncFileDictTree[domain].keys())[0]
    else:
        model = str(arguments["model"])
    if "exhaust-level" not in arguments:
        experiment = list(ncFileDictTree[domain][model].keys())[0]
    else:
        experiment = str(arguments["exhaust-level"])
    # ---------------

    requestedFiles = getList(ncFileDictTree,
                             domain,
                             model,
                             experiment,
                             variable)

    for ncFile in requestedFiles:
        if fromDate > ncFile.getStartDate()\
                and toDate < ncFile.getLastDate():
                    # If returnArea is None, it is not within file
                    returnArea = ncFile.getData(dimension,
                                                fromDate,
                                                toDate,
                                                fromLat,
                                                toLat,
                                                fromLong,
                                                toLong,
                                                returnDimension)

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
