#!/usr/bin/env python3

from defaults import *
from thor.routes import thorApp
import thor.const as const
import thor.util as util
import sys
import logging
import thor.frozendict as frozendict


printTree = False
# Read arguments from command line
for argument in sys.argv:
    if "--help" in argument or "-h" in argument:
        util.printHelp(sys.argv[0])
        sys.exit(1)
    elif "--app-name=" in argument:
        appName = argument.replace("--app-name", "")
    elif "--debug" == argument:
        logLevel = logging.DEBUG
    elif "--netCDF-folder=" in argument:
        ncFolder = argument.replace("--netCDF-folder=", "")
    elif "--log-file=" in argument:
        logFiles.append(argument.replace("--log-file=", ""))
    elif "--print-tree" in argument:
        printTree = True
# appName and subfolder to read netCDF files from
const.appName = appName

# Create a logger that outputs to console and supplied log-files
const.log = logging.getLogger(const.appName)
const.log.setLevel(logLevel)
consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logLevel)
formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
consoleHandler.setFormatter(formatter)
const.log.addHandler(consoleHandler)
for logFile in logFiles:
    fileHandler = logging.FileHandler(logFile)
    fileHandler.setLevel(logLevel)
    fileHandler.setFormatter(formatter)
    const.log.addHandler(fileHandler)

# Load ncFiles
const.ncFolder = ncFolder
const.ncFiles = frozendict.FrozenDict(util.openFiles(ncFolder))
if printTree:
    util.printTree(ncFolder)

# This defines valid arguments for API
const.apiMustArgs = apiMustArgs
const.apiOptionalArgs = apiOptionalArgs

if __name__ == "__main__":
    thorApp.run()

