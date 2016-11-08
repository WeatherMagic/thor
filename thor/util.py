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
    ncFiles = []

    for currentFile in files:
        if currentFile.endswith(".nc"):
            const.log.info("Loading netCDF file: " +
                           folder + os.sep + currentFile)
            ncFiles.append(reader.Reader(folder + os.sep + currentFile,
                                         const.nmbZoomLevels))

    # Return touple since immutable
    return tuple(ncFiles)
