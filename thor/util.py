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


def printHelp(execName):
    print("Thor - bringer of weather")
    print("")
    print("Usage: ")
    print("    " + execName +
          " [--debug] [--app-name=appName] \
[--netCDF-folder=folder] [--log-file=logFile] [--print-tree]")
    print("")
    print("Default values for all arguments can \
be found (and set) in the file defaults.py.")
    print("")


def argumentsHandler(arguments):
    failure = False
    missingArgs = []

    # Check that request includes all arguments
    for arg in const.apiMustArgs:
        if arg not in arguments:
            failure = True
            missingArgs.append(arg)

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
    elif "to-month" not in arguments:
        arguments["to-month"] = arguments["from-month"]

    if "to-year" not in arguments:
        arguments["to-year"] = arguments["from-year"]

    arguments["from-date"] = datetime.strptime(str(arguments["from-year"]) +
                                               str(arguments["from-month"]) +
                                               "1",
                                               "%Y%m%d")
    arguments["to-date"] = datetime.strptime(str(arguments["to-year"]) +
                                             str(int(arguments[
                                                 "to-month"])) +
                                             "1",
                                             "%Y%m%d")

    if arguments["from-date"] > arguments["to-date"]:
        return {"ok":
                False,
                "error":
                "from-date larger than to-date."}

    # ---------------------------------------

    # Handling returnDimension
    if isinstance(arguments["return-dimension"], str):
        retDim = arguments["return-dimension"].replace("[", "")
        retDim = retDim.replace("]", "")
        retDim = retDim.split(", ")
        arguments["return-dimension"] = retDim

    if len(arguments["return-dimension"]) < 2:
        return {"ok":
                False,
                "error":
                "return-dimension contains to few dimensions."}

    # We need this since we need integers in return dimension
    intReturnDimension = []
    for arg in arguments["return-dimension"]:
        int_arg = 0

        try:
            int_arg = int(arg)
            intReturnDimension.append(int_arg)
        except ValueError:
            return {"ok":
                    False,
                    "error":
                    "return-dimension contains non-integers."}

        if int_arg < 1:
            return {"ok":
                    False,
                    "error":
                    "return-dimension contains non-positive dimension count."}
    # Save as integers
    arguments["return-dimension"] = intReturnDimension

    if len(arguments["return-dimension"]) == 2:
        arguments["return-dimension"] = np.array(arguments[
            "return-dimension"])
    else:
        return {"ok": False,
                "error":
                "returnDimension doesn't contain two values."}

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

    arguments["ok"] = True
    return arguments


def printTree(folder):
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

    print(json.dumps(domainDict,
                     sort_keys=True,
                     indent=4,
                     separators=(',', ': ')))


def openFiles(folder):
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
    vector[:pad_width[0]] = 0
    vector[-pad_width[1]:] = 0
    return vector


def padWithOnes(vector, pad_width, iaxis, kwargs):
    vector[:pad_width[0]] = 1
    vector[-pad_width[1]:] = 1
    return vector


def padWithMinusOneTwoEight(vector, pad_width, iaxis, kwargs):
    vector[:pad_width[0]] = -128
    vector[-pad_width[1]:] = -128
    return vector


def convertToPNGRange(data, variable):
    borderValue = 0
    data = np.ma.masked_greater(data, 10000)

    # Kelvin->Celsius and fit into PNG 8-bit integer range (0 to 255)
    if variable == "temperature":
        # Set 0 degrees Celsius around 64
        # -273 + 64 = -209 degrees
        data = data - 209
        borderValue = 127

    elif variable == "precipitation":
        # Convert from kg/(m^2*s) to kg/(m^2*d) = mm/d
        # 3600s/h * 24h/d = 86400s/d
        data = data * 86400
        borderValue = 63

    # Get a mask that'll be the alpha channel
    maskArray = data.mask
    if maskArray:
        # Fit to integer range
        maskArray = maskArray.astype("uint8")
        # PAd with ones
        maskArray = np.lib.pad(maskArray, 1, padWithOnes)
        # Convert to PNG alpha range
        maskArray = (255-255*maskArray)

    # Set border in order to fix PNG res
    data = data.clip(0, borderValue)
    data = data.astype("uint8")
    print("hit3")
    data = np.lib.pad(data, 1, padWithZeros)
    data[0, 0] = borderValue
    # Create an array with four channels (RGBA PNG)
    dimensions = data.shape
    outData = np.ndarray(shape=(dimensions[0],
                                dimensions[1],
                                4),
                         dtype="uint8")
    outData[:, :, 0] = data[:, :]
    outData[:, :, 1] = 0
    outData[:, :, 2] = 0
    if maskArray:
        outData[:, :, 3] = maskArray[:, :]
    else:
        outData[:, :, 3] = 255
        
    return outData
