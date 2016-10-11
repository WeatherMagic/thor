#!/usr/bin/env python3

import thor.reader as reader
import thor.const as const
import os

def openFiles(folder):
    files = os.listdir(folder)
    ncFiles = []
    
    for currentFile in files:
        if currentFile.endswith(".nc"):
            const.log.info("Loading netCDF file: " + folder + os.sep + currentFile)
            ncFiles.append(reader.Reader(folder + os.sep + currentFile))
    
    return ncFiles

