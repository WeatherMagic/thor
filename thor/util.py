#!/usr/bin/env python3

import thor.reader as reader
import thor.const as const
import os


def checkArguments(arguments):
    mustArgs = ["zoom-level",
                "longitude",
                "latitude",
                "year"]

    for arg in mustArgs:
        if arg not in arguments:
            return {"ok": False, "error": "Missing non-optional argument " + arg + "!"}


def openFiles(folder):
    files = os.listdir(folder)
    ncFiles = []
    
    for currentFile in files:
        if currentFile.endswith(".nc"):
            const.log.info("Loading netCDF file: " + folder + os.sep + currentFile)
            ncFiles.append(reader.Reader(folder + os.sep + currentFile))
    
    return ncFiles

