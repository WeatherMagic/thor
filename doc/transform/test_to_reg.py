#!/usr/bin/env python3

import sys
from numpy import *
from thor.transform import *
import netCDF4


rlon = float(sys.argv[1]) #ncFile.variables['rlat'][0]
rlat = float(sys.argv[2]) #ncFile.variables['rlon'][0]

print("rlon: " + str(rlon) + " rlat: " + str(rlat))

latLon = toReg(rlon, rlat)

print("lon: " + str(latLon.item(0, 0)) + " lat: " + str(latLon.item(1,0)))

latLon = toRot(latLon.item(0, 0), latLon.item(1, 0))

print("rlon: " + str(latLon.item(0, 0)) + "rlat: " + str(latLon.item(1,0)))


