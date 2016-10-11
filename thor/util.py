#!/usr/bin/env python3

import thor.reader as reader
import thor.const as const
import os


def checkArguments(arguments):
    mustArgs = ["zoom-level",
                "longitude",
                "latitude",
                "year"]
    failure = False
    missingArgs = []

    for arg in mustArgs:
        if arg not in arguments:
            failure = True
            missingArgs.append(arg)
    
    if failure:
        errorMessage = ""
        for arg in missingArgs:
            errorMessage += arg
            if arg != missingArgs[-1] and arg != missingArgs[-2]:
                errorMessage += ", "
            elif arg == missingArgs[-2] and len(missingArgs) != 1:
                errorMessage += " and "
        return {"ok": False, "error": "Missing non-optional argument(s) " + errorMessage + "!"}
    
    return {"ok": True}


def openFiles(folder):
    files = os.listdir(folder)
    ncFiles = []
    
    for currentFile in files:
        if currentFile.endswith(".nc"):
            const.log.info("Loading netCDF file: " + folder + os.sep + currentFile)
            ncFiles.append(reader.Reader(folder + os.sep + currentFile))
    
    return ncFiles

