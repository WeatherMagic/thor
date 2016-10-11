#!/usr/bin/env python3

from thor.routes import thorApp
import thor.const as const
import thor.init
import sys
import logging


if __name__ == "__main__":
    
    appName = "thor"
    logLevel = logging.WARNING
    ncFolder = "ncFiles"

    for argument in sys.argv:
        if "--app-name=" in argument:
            appName = argument.replace("--app-name", "")
        elif "--debug" == argument:
            logLevel = logging.DEBUG
        elif "--netCDF-folder=" in argument:
            ncFolder = argument.replace("--netCDF-folder=")
    
    # appName and subfolder to read netCDF files from
    const.ncFolder = ncFolder
    const.appName = appName
    # Logging
    const.log = logging.getLogger(const.appName)
    const.log.setLevel(logLevel)
    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(logLevel)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    consoleHandler.setFormatter(formatter)
    const.log.addHandler(consoleHandler)
    # Load ncFiles
    const.ncFiles = thor.init.openFiles(const.ncFolder)
    
    thorApp.run()
