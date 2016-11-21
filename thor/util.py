#!/usr/bin/env python3

import thor.reader as reader
import thor.const as const
import os
import thor.frozendict as frozendict


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

                domainDict[currentFile.getDomain()][currentFile.getModel()] = experimentDict

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
    # TODO: This sometimes works, sometimes does not. Might be a bug in Python or FrozenDict
    # Create tuples of all lists, making them immutable
#    for domain, modelDict in domainDict.items():
#        for model, expDict in modelDict.items():
#            for experiment, variableDict in expDict.items():
#                for variable, readerList in variableDict.items():
#                    variableDict[variable] = tuple(readerList)
#                experimentDict[experiment] = frozendict.FrozenDict(variableDict)
#            modelDict[model] = frozendict.FrozenDict(experimentDict)
#        domainDict[domain] = frozendict.FrozenDict(modelDict)

    # Return a froxen dict structure
    return frozendict.FrozenDict(domainDict)
