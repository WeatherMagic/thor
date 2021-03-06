#!/usr/bin/env python3

import thor.reader as reader
import thor.const as const
import os
import thor.frozendict as frozendict
from datetime import datetime
from datetime import timedelta
import numpy as np
import json
import copy
from math import floor


def printHelp(execName):
    """
    Prints how python can be interacted with in terminal.
    """
    print("Thor - bringer of weather")
    print("")
    print("Usage: ")
    print("    " + execName +
          " [--disable-cache] [--debug] [--app-name=appName] \
[--netCDF-folder=folder] [--log-file=logFile] [--print-tree]")
    print("")
    print("Default values for all arguments can \
be found (and set) in the file defaults.py.")
    print("")


def argumentsHandler(arguments):
    """
    Checks so that the arguments given in a request to Thor follows
    the Thor API.
    """
    failure = False
    missingArgs = []

    # Check that request includes all arguments
    for arg in const.apiMustArgs:
        if arg not in arguments:
            failure = True
            missingArgs.append(arg)
    # Check that the request only contains arguments
    # that's valid
    validArgs = const.apiMustArgs + const.apiOptionalArgs
    for arg in arguments:
        if arg not in validArgs:
            return {"ok": False,
                    "error": "Use of non-valid argument " + arg + "!"
                    }

    # If not, format a human readable error message
    if failure:
        errorMessage = ""
        for arg in missingArgs:
            errorMessage += arg
            if arg != missingArgs[-1] and arg != missingArgs[-2]:
                errorMessage += ", "
            elif len(missingArgs) != 1 and arg == missingArgs[-2]:
                errorMessage += " and "
        return {"ok":
                False,
                "error":
                "Missing non-optional argument(s) " + errorMessage + "!"}

    # ---------------------------------------

    # Handeling time
    try:
        arguments["to-month"] = int(arguments["month"])
        arguments["year"] = int(arguments["year"])
    except ValueError as e:
        return {"ok": False,
                "error": "Month and year needs to integers!"
                }

    if arguments["to-month"] < 1 or arguments["to-month"] > 12:
        return {"ok": False,
                "error": "Month has to be an integer between 1 and 12!"
                }

    if arguments["year"] < 1950 or arguments["year"] > 2100:
        return {"ok": False,
                "error": "Year has to be between 1950 and 2100!"
                }

    arguments["from-date"] = datetime(arguments["year"],
                                      arguments["to-month"], 1)
    # ---------------------------------------

    # Handling latitude
    try:
        arguments["from-latitude"] = float(arguments["from-latitude"])
        arguments["to-latitude"] = float(arguments["to-latitude"])
    except ValueError:
        return {"ok":
                False,
                "error":
                "To or from latitude contains something that is not a number."}

    if arguments["to-latitude"] < arguments["from-latitude"]:
        return {"ok":
                False,
                "error":
                "from-latitude larger than to-latitude."}

    if arguments["from-latitude"] < -90:
        return {"ok":
                False,
                "error":
                "from-latitude is smaller than -90."}
    if arguments["to-latitude"] > 90:
        return {"ok":
                False,
                "error":
                "to-latitude is larger than 90."}

    # ---------------------------------------

    # Handling longitude
    try:
        arguments["from-longitude"] = float(arguments["from-longitude"])
        arguments["to-longitude"] = float(arguments["to-longitude"])
    except ValueError:
        return {"ok":
                False,
                "error":
                "To or from longitude contains" +
                " something that is not a number."}

    if arguments["to-longitude"] < arguments["from-longitude"]:
        return {"ok":
                False,
                "error":
                "from-longitude larger than to-longitude."}

    if arguments["from-longitude"] < -180:
        return {"ok":
                False,
                "error":
                "from-longitude is smaller than -180."}
    if arguments["to-longitude"] > 180:
        return {"ok":
                False,
                "error":
                "to-latitude is larger than 180."}

    try:
        arguments["height-resolution"] = int(arguments["height-resolution"])
    except ValueError:
        return {"ok": False,
                "error":
                "height-resolution contains something that is not a number."}

    # -------------------------------------
    """
     Decide the return size of the image to put on earth.
     This is to simplify for front-end since they don't
     need to take lon-lat res scaling into account
    """
    lenLat = arguments["to-latitude"] - arguments["from-latitude"]
    lenLon = arguments["to-longitude"] - arguments["from-longitude"]

    resLat = arguments["height-resolution"]

    if lenLat == 0.0 or lenLon == 0.0:
        return{"ok": False,
               "error": "Latitude or longitude range is zero"}

    resLon = floor(lenLon/lenLat*resLat)
    # Ugly as fuck fix for no key-hole-shape on earth
    # in weather-front if we ask for entire planet
    if lenLon == 360:
        resLon = resLon + 4

    arguments["return-dimension"] = [resLat,
                                     resLon]

    arguments["ok"] = True
    return arguments


def getTreeAsString(folder):
    """
    Returns a string with the netCDF file tree that Thor currently has loaded.
    """
    domainDict = openFiles(folder)
    for domain, modelDict in domainDict.items():
        for model, expDict in modelDict.items():
            for experiment, variableDict in expDict.items():
                for variable, readerList in variableDict.items():
                    for i in range(0, len(readerList)):
                        readerList[i] = readerList[i].getVariable()\
                                + ": "\
                                + str(readerList[i].getStartDate())[0:10]\
                                + " - "\
                                + str(readerList[i].getLastDate())[0:10]
    return domainDict


def printTree(folder):
    """
    Prints the netCDF file tree that Thor currently has loaded.
    """

    print(json.dumps(getTreeAsString(folder),
                     sort_keys=True,
                     indent=4,
                     separators=(',', ': ')))


def openFiles(folder):
    """
    Returns a dict tree with all the files Thor currently has loaded.
    The tree has the following levels to get to the netCDF files
    located in a leaf node lists.
    Tree-
        |Domains-
               |Models-
                     |Exhaust-levels-
                                    |Variables-
                                              |Files
    """
    files = os.listdir(folder)
    domainDict = dict()

    for currentFile in files:
        if currentFile.endswith(".nc"):
            const.log.info("Loading netCDF file: " +
                           folder + os.sep + currentFile)
            currentFile = reader.Reader(folder + os.sep + currentFile)

            # Can't find domain in the domainDict
            # therfore I add the domain as key and
            # the variableDict as value in the domainDict
            if currentFile.getDomain() not in domainDict.keys():

                readerList = [currentFile]
                variableDict = {currentFile.getVariable(): readerList}
                experimentDict = {currentFile.getExperiment(): variableDict}
                modelDict = {currentFile.getModel(): experimentDict}

                domainDict[currentFile.getDomain()] = modelDict

            # Can't find model in the modelDict
            # therefore I add the model as key
            # and the experimentDict as value in the modelDict
            elif currentFile.getModel() not in domainDict[
                    currentFile.getDomain()].keys():

                readerList = [currentFile]
                variableDict = {currentFile.getVariable(): readerList}
                experimentDict = {currentFile.getExperiment(): variableDict}

                domainDict[
                    currentFile.getDomain()][
                        currentFile.getModel()] = experimentDict

            # Can't find the experiment in the experimentDict
            # therefore I add the experiment as key
            # and the readerList as value in the experimentDict
            elif currentFile.getExperiment() not in domainDict[
                    currentFile.getDomain()][
                        currentFile.getModel()].keys():

                readerList = [currentFile]
                variableDict = {currentFile.getVariable(): readerList}

                domainDict[currentFile.getDomain()][
                        currentFile.getModel()][
                                currentFile.getExperiment()] = variableDict

            # Can't find variable in the variableDict
            # therefore I add the variable as key
            # and the modelDict as value in the variableDict
            elif currentFile.getVariable() not in domainDict[
                    currentFile.getDomain()][
                        currentFile.getModel()][
                            currentFile.getExperiment()].keys():

                readerList = [currentFile]

                domainDict[
                    currentFile.getDomain()][
                        currentFile.getModel()][
                            currentFile.getExperiment()][
                                currentFile.getVariable()] = readerList

            # I have found my way down to the leaf children and can append
            # the readerList with the currentFileReader
            else:
                domainDict[
                    currentFile.getDomain()][
                        currentFile.getModel()][
                            currentFile.getExperiment()][
                                currentFile.getVariable()].append(
                                    currentFile)
    # Return a froxen dict structure
    return domainDict


def padWithZeros(vector, pad_width, iaxis, kwargs):
    """
    Purpose: Pad a numpy array with zeros
    """
    vector[:pad_width[0]] = 0
    vector[-pad_width[1]:] = 0
    return vector


def padWithOnes(vector, pad_width, iaxis, kwargs):
    """
    Purpose: Pad a numpy array with ones
    """
    vector[:pad_width[0]] = 1
    vector[-pad_width[1]:] = 1
    return vector


def padWithMinusOneTwoEight(vector, pad_width, iaxis, kwargs):
    """
    Purpose: Pad a numpy array with minus 128
    """
    vector[:pad_width[0]] = -128
    vector[-pad_width[1]:] = -128
    return vector


def convertToPNGRange(data, variable, fromLong, toLong, fromLat, toLat):
    """
    Purpose: Convert a numpy array into PNG range
    that works for our data variables and
    are readable for weather-front.
    """
    borderValue = 0
    multiplier = 0
    pad = True

    # If entire earth - don't pad
    # This hole pad/no-pad shit is
    # in order to fix bugs in weather-front
    # and has nothing to do with API/thor
    if fromLong == -180 and toLong == 180:
        pad = False

    # Kelvin->Celsius and fit into PNG 8-bit integer range (0 to 255)
    if variable == "temperature":
        # Set 0 degrees Celsius around 64
        # -273 + 64 = -209 degrees
        data = data - 209
        borderValue = 127.5
        multiplier = 2

    elif variable == "precipitation":
        # Convert from kg/(m^2*s) to kg/(m^2*d) = mm/d
        # 3600s/h * 24h/d = 86400s/d
        # Then half of it to
        data[data.mask == False] = data[data.mask == False] * 86400
        borderValue = 63.75
        multiplier = 4

    # Get a mask that'll be the alpha channel
    maskArray = data.mask
    maskArray = maskArray.astype("uint8")
    if pad:
        maskArray = np.lib.pad(maskArray, 1, padWithOnes)
    # Convert to alpha
    maskArray = (255-255*maskArray)

    # Set border in order to fix PNG res
    data = data.clip(0, borderValue)

    if pad:
        data = np.lib.pad(data, 1, padWithZeros)
    # If we don't pad - compensate by inserting a zero
    if not pad:
        data[0, 2] = 0
    data[0, 3] = borderValue

    data = data * multiplier
    data = data.astype("uint8")
    # Create an array with four channels (RGBA PNG)
    dimensions = data.shape
    if not pad:
        longScale = (toLong - fromLong) / (toLat - fromLat)
        dimensions = [dimensions[0], int(longScale*dimensions[0])]
    outData = np.ndarray(shape=(dimensions[0],
                                dimensions[1],
                                4),
                         dtype="uint8")
    if pad:
        outData[:, :, 0] = data[:, :]
        outData[:, :, 3] = maskArray[:, :]
    else:
        outData[:, :, 0] = data[:, 2:dimensions[1]+2]
        outData[:, :, 3] = maskArray[:, 2:dimensions[1]+2]
    outData[:, :, 1] = 0
    outData[:, :, 2] = 0

    return outData
