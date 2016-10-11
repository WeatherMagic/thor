#!/usr/bin/env python3

import logging


appName = "thor"

logLevel = logging.WARNING
logFiles = []

ncFolder = "ncFiles"

apiMustArgs = ["zoom-level",
               "longitude",
               "latitude",
               "year"]
apiOptionalArgs = ["month"]
