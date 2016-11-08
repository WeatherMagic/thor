#!/usr/bin/env python3

import logging


appName = "thor"

logLevel = logging.WARNING
logFiles = ()

ncFolder = "ncFiles"

apiMustArgs = ("zoom-level",
               "from-year",
               "to-year",
               "from-longitude",
               "from-latitude",
               "to-latitude",
               "to-longitude")
apiOptionalArgs = ("from-month", "to-month")
