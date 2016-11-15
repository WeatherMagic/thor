#!/usr/bin/env python3

import thor.reader as reader
import thor.const as const
import os


def printHelp(execName):
    print("Thor - bringer of weather")
    print("")
    print("Usage: ")
    print("    " + execName +
          " [--debug] [--app-name=appName] \
[--netCDF-folder=folder] [--log-file=logFile]")
    print("")
    print("Default values for all arguments can \
be found (and set) in the file defaults.py.")
    print("")


def checkArguments(arguments):
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
        return {
                "ok":
                False,
                "error":
                "Missing non-optional argument(s) " + errorMessage + "!"}

    return {"ok": True}


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
                experiamentDict = {currentFile.getExperiment(): readerList}
                modelDict = {currentFile.getModel(): experiamentDict}
                variableDict = {currentFile.getVariable(): modelDict}
                domainDict[currentFile.getDomain()] = variableDict

            # Can't find variable in the variableDict
            # therefore I add the variable as key
            # and the modelDict as value in the variableDict
            elif currentFile.getVariable() not in domainDict[
                    currentFile.getDomain()].keys():

                readerList = [currentFile]
                experiamentDict = {currentFile.getExperiment(): readerList}
                modelDict = {currentFile.getModel(): experiamentDict}
                domainDict[
                    currentFile.getDomain()][
                        currentFile.getVariable()] = modelDict

            # Can't find model in the modelDict
            # therefore I add the model as key
            # and the experiamentDict as value in the modelDict
            elif currentFile.getModel() not in domainDict[
                    currentFile.getDomain()][
                        currentFile.getVariable()].keys():

                readerList = [currentFile]
                experiamentDict = {currentFile.getExperiment(): readerList}
                domainDict[
                    currentFile.getDomain()][
                        currentFile.getVariable()][
                            currentFile.getModel()] = experiamentDict

            # Can't find the experiament in the experiamentDict
            # therefore I add the experiament as key
            # and the readerList as value in the experiamentDict
            elif currentFile.getExperiment() not in domainDict[
                    currentFile.getDomain()][
                        currentFile.getVariable()][
                            currentFile.getModel()].keys():

                readerList = [currentFile]
                domainDict[currentFile.getDomain()][
                    currentFile.getVariable()][
                        currentFile.getModel()][
                            currentFile.getExperiment()] = readerList

            # I have found my way down to the leaf children and can append
            # the readerList with the currentFileReader
            else:
                domainDict[
                    currentFile.getDomain()][
                        currentFile.getVariable()][
                            currentFile.getModel()][
                                currentFile.getExperiment()].append(
                                    currentFile)

    return domainDict
