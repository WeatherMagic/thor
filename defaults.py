#!/usr/bin/env python3

import logging


appName = "thor"

logLevel = logging.WARNING
logFiles = ()

ncFolder = "ncFiles"

apiMustArgs = ("month",
               "year",
               "from-longitude",
               "from-latitude",
               "to-latitude",
               "to-longitude",
               "height-resolution",
               "climate-model",
               "exhaust-level"
               )
apiOptionalArgs = (
        )
