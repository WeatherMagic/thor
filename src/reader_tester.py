#!/usr/bin/env python3 

import reader
import datetime

nc_data = reader.Reader("2001-11-01_2001-12-31.nc")

fromDate = datetime.datetime.strptime("2001-11-22", "%Y-%m-%d")
toDate = datetime.datetime.strptime("2001-12-1", "%Y-%m-%d")

print(nc_data.getSurfaceTemp(0, 70, 0, 70, fromDate, toDate))
