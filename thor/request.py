#!/usr/bin/env python3

import thor.reader as reader
import thor.sigProcess as sigProcess
from datetime import datetime
from datetime import timedelta
import numpy as np
import logging
from math import floor
import thor.util as util


def getClimateModels(ncFileTree, arguments, ncFolder):
    """
    Purpose: Get response on client question to server
    asking which variables that are available within
    the dataset.
    """
    returnData = {}
    returnData["domains"] = []
    returnData["models"] = []
    returnData["exhaust-levels"] = []

    for domain, modelDict in ncFileTree.items():
        if domain not in returnData["domains"]:
            returnData["domains"].append(domain)
        for model, experimentDict in modelDict.items():
            if model not in returnData["models"]:
                returnData["models"].append(model)
            for experiment in experimentDict.keys():
                if experiment not in returnData["exhaust-levels"]:
                    returnData["exhaust-levels"].append(experiment)

    if arguments["with-tree"]:
        returnData["tree"] = util.getTreeAsString(ncFolder)

    returnData["ok"] = True
    return returnData


def getReaderList(dictTree,
                  model,
                  experiment,
                  variable):
    """
    Get the leaf of a certain tree path.
    The leaf is a list of readers which
    gives access to data from a NetCDF file
    """
    returnList = []
    for domain in dictTree:
        if model in list(dictTree[domain].keys()) and\
           experiment in list(dictTree[domain][model].keys()) and\
           variable in list(dictTree[domain][model][experiment].keys()):
            nextDomain = dictTree[domain][model][experiment][variable]
            returnList = returnList + nextDomain
    return returnList


def overlapScale(overlapArea,
                 fromLat,
                 toLat,
                 fromLong,
                 toLong):
    """
    Get the quota between the length of the
    borders of the requested area and the data
    within this file.
    """
    def scale(oldFrom,
              oldTo,
              newFrom,
              newTo):
        return (newTo-newFrom)/(oldTo-oldFrom)

    return (scale(fromLat,
                  toLat,
                  overlapArea[0],
                  overlapArea[1]),
            scale(fromLong,
                  toLong,
                  overlapArea[2],
                  overlapArea[3]))


def handleRequest(arguments, ncFileDictTree, log):
    """
    Purpose: Once all arguments are found to be
    valid according to API - start working on
    colllecting the data and return it.
    """
    variable = arguments["variable"]
    model = str(arguments["climate-model"])
    experiment = str(arguments["exhaust-level"])

    # ---------------
    requestedFiles = getReaderList(ncFileDictTree,
                                   model,
                                   experiment,
                                   variable)

    if len(requestedFiles) == 0:
        return {"ok": False,
                "error": "No files found with specified variable, " +
                "climate-model, exhaust-level."}

    returnData = np.ndarray(shape=arguments["return-dimension"],
                            dtype=float)

    returnData = np.ma.array(returnData, mask=True)

    fillFlag = False

    for ncFile in requestedFiles:
        # If request within time period for file
        if arguments["from-date"] > ncFile.getStartDate()\
           and arguments["from-date"] < ncFile.getLastDate():
            climateAreaDict = ncFile.getData(
                arguments["from-date"],
                arguments["from-date"],
                arguments["from-latitude"],
                arguments["to-latitude"],
                arguments["from-longitude"],
                arguments["to-longitude"])

            # Did we get any data from the file?
            # If so, take overlap between file and
            # requested area
            if climateAreaDict["ok"]:
                [latScale,
                 lonScale] = overlapScale(climateAreaDict["area"],
                                          arguments["from-latitude"],
                                          arguments["to-latitude"],
                                          arguments["from-longitude"],
                                          arguments["to-longitude"])

                latInterpolLen = floor(arguments["return-dimension"][0] *
                                       latScale)
                lonInterpolLen = floor(arguments["return-dimension"][1] *
                                       lonScale)

                # Interpolating the data
                returnAreaDict = sigProcess.interpolate(
                    climateAreaDict["data"],
                    [1,
                     latInterpolLen,
                     lonInterpolLen])

                if returnAreaDict["ok"]:

                    latStart = floor((((climateAreaDict["area"][0] -
                                        arguments["from-latitude"]) *
                                       arguments["return-dimension"][0]) /
                                      (arguments["to-latitude"] -
                                       arguments["from-latitude"])))

                    lonStart = floor((((climateAreaDict["area"][2] -
                                        arguments["from-longitude"]) *
                                       arguments["return-dimension"][1]) /
                                      (arguments["to-longitude"] -
                                       arguments["from-longitude"])))

                    fillFlag = True

                    areaData = np.ma.masked_greater(
                        returnAreaDict["data"], 10000)

                    origMask = returnData.mask[latStart:latStart +
                                               latInterpolLen,
                                               lonStart:lonStart +
                                               lonInterpolLen]

                    cutMask = np.logical_and(origMask,
                                             np.logical_not(areaData.mask))

                    tempReturnData = returnData[latStart:latStart +
                                                latInterpolLen,
                                                lonStart:lonStart +
                                                lonInterpolLen]

                    tempReturnData.data[
                        cutMask == True] = areaData[
                            cutMask == True]

                    returnData.data[latStart:latStart +
                                    latInterpolLen,
                                    lonStart:lonStart +
                                    lonInterpolLen] = tempReturnData
                    returnData.mask[latStart:latStart +
                                    latInterpolLen,
                                    lonStart:lonStart +
                                    lonInterpolLen] = np.logical_and(
                                        origMask,
                                        areaData.mask)
    if fillFlag:
        return {"ok": True,
                "data": returnData}
    else:
        return {"ok": False,
                "error": "No data in specified area"}
