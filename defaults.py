#!/usr/bin/env python3

import logging


appName = "thor"

logLevel = logging.WARNING
logFiles = ()

ncFolder = "ncFiles"

apiMustArgs = ("zoom-level",
               "from-longitude",
               "from-latitude",
               "year",
               "to-latitude",
               "to-longitude")
apiOptionalArgs = ("month")
