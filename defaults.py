#!/usr/bin/env python3

import logging


appName = "thor"

logLevel = logging.WARNING
logFiles = ()

ncFolder = "ncFiles"

apiMustArgs = ("from-year",
               "from-longitude",
               "from-latitude",
               "to-latitude",
               "to-longitude",
               "return-dimension")
apiOptionalArgs = ("from-month",
                   "to-month",
                   "to-year",
                   "domain",
                   "climate-model"
                   "exhaust-level")
