#!/usr/bin/env python3

import thor.reader as reader
import thor.sigProcess as sigProcess
from datetime import datetime
from datetime import timedelta
import numpy as np
import logging


def getList(dictTree,
            model,
            experiment,
            variable):
    returnList = []
    for domain in dictTree:
        if model in list(dictTree[domain].keys()) and\
           experiment in list(dictTree[domain][model].keys()) and\
           variable in list(dictTree[domain][model][experiment].keys()):
            nextDomain = dictTree[domain][model][experiment][variable]
            returnList = returnList + nextDomain
    return returnList


def handleRequest(arguments, ncFileDictTree, log):

    # ---------------
    """ TODO: Until we expose different climate models within the API
     - we just set default values for them """
    variable = arguments["variable"]
    if "domain" not in arguments:
        domain = list(ncFileDictTree.keys())[0]
    elif arguments["domain"] not in list(ncFileDictTree.keys()):
        return {"ok": False,
                "error": "No files with specified domain."}
    else:
        domain = str(arguments["domain"])
    if "climate-model" not in arguments:
        model = list(ncFileDictTree[domain].keys())[0]
    elif arguments["climate-model"] not in list(ncFileDictTree[
            domain].keys()):
        return {"ok": False,
                "error": "No files with specified climate-model."}
    else:
        model = str(arguments["climate-model"])
    if "exhaust-level" not in arguments:
        experiment = list(ncFileDictTree[domain][model].keys())[0]
    elif arguments["exhaust-level"] not in list(ncFileDictTree[
            domain][model].keys()):
        return {"ok": False,
                "error": "No files with specified exhaust-level."}
    else:
        experiment = str(arguments["exhaust-level"])

    # ---------------
    requestedFiles = getList(ncFileDictTree,
                             model,
                             experiment,
                             variable)

    returnData = np.ndarray(shape=arguments["return-dimension"],
                            dtype=float)
    returnData.fill(100000)

    for ncFile in requestedFiles:
        if arguments["from-date"] > ncFile.getStartDate()\
           and arguments["to-date"] < ncFile.getLastDate():

                climateAreaDict = ncFile.getData(
                    arguments["from-date"],
                    arguments["to-date"],
                    arguments["from-latitude"],
                    arguments["to-latitude"],
                    arguments["from-longitude"],
                    arguments["to-longitude"])

                if not climateAreaDict["ok"]:
                    return climateAreaDict

            # Interpolating the data
                returnAreaDict = sigProcess.interpolate(
                    climateAreaDict["data"],
                    arguments["return-dimension"])

                if not returnAreaDict["ok"]:
                    return returnAreaDict

                return {"ok": True,
                        "data": returnAreaDict["data"]}

    return {"ok": False,
            "error":
            "Specified date range not within server dataset."}

