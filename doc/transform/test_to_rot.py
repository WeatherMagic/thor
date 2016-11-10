#!/usr/bin/env python3

import sys
from numpy import *
from thor.transform import *
import netCDF4


lon = float(sys.argv[1]) #ncFile.variables['rlat'][0]
lat = float(sys.argv[2]) #ncFile.variables['rlon'][0]

print("lon: " + str(lon) + " lat: " + str(lat))

latLon = toRot(lon, lat)

print("rlon: " + str(latLon.item(0, 0)) + " rlat: " + str(latLon.item(1,0)))

latLon = toReg(latLon.item(0, 0), latLon.item(1, 0))

print("lon: " + str(latLon.item(0, 0)) + "lat: " + str(latLon.item(1,0)))


