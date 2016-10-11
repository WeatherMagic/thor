#!/usr/bin/env python3

from defaults import *
import thor.routes as routes
import thor.const as const
import thor.util as util
import sys
import logging


if __name__ == "__main__":
    # Read arguments from command line
    for argument in sys.argv:
        if "--app-name=" in argument:
            appName = argument.replace("--app-name", "")
        elif "--debug" == argument:
            logLevel = logging.DEBUG
        elif "--netCDF-folder=" in argument:
            ncFolder = argument.replace("--netCDF-folder=", "")
        elif "--log-file=" in argument:
            logFiles.append(argument.replace("--log-file=", ""))
    
    # appName and subfolder to read netCDF files from
    const.appName = appName

    # Create a logger that outputs to console and supplied log-files
    const.log = logging.getLogger(const.appName)
    const.log.setLevel(logLevel)
    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(logLevel)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    consoleHandler.setFormatter(formatter)
    const.log.addHandler(consoleHandler)
    for logFile in logFiles:
        fileHandler = logging.FileHandler(logFile)
        fileHandler.setLevel(logLevel)
        fileHandler.setFormatter(formatter)
        const.log.addHandler(fileHandler)
    
    # Load ncFiles
    const.ncFiles = util.openFiles(ncFolder)
    
    # This defines valid arguments for API
    const.apiMustArgs = apiMustArgs
    const.apiOptionalArgs = apiOptionalArgs
    
    # Run app!
    routes.thorApp.run()
