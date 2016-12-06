#!/usr/bin/env python3

import thor.reader as reader
import thor.sigProcess as sigProcess
from datetime import datetime
from datetime import timedelta
import numpy as np
import logging
from math import floor


def getReaderList(dictTree,
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


def overlapScale(overlapArea,
                 fromLat,
                 toLat,
                 fromLong,
                 toLong):

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
        if arguments["from-date"] > ncFile.getStartDate()\
           and arguments["from-date"] < ncFile.getLastDate():
            climateAreaDict = ncFile.getData(
                arguments["from-date"],
                arguments["from-date"],
                arguments["from-latitude"],
                arguments["to-latitude"],
                arguments["from-longitude"],
                arguments["to-longitude"])

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
