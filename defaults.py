#!/usr/bin/env python3

import logging


appName = "thor"

logLevel = logging.WARNING
logFiles = ()

ncFolder = "ncFiles"

apiMustArgs = ("zoom-level",
               "fromLongitude",
               "fromLatitude",
               "year",
               "toLatitude",
               "toLongitude")
apiOptionalArgs = ("month")
nmbZoomLevels = 100
