#!/usr/bin/env python3

import sys
from numpy import *
from thor.transform import *
import netCDF4

filename = "ncFiles/tas_EUR-11_CNRM-CERFACS-CNRM-CM5_rcp45_r1i1p1_SMHI-RCA4_v1_mon_200601-201012.nc"
ncFile = netCDF4.Dataset(filename, 'r')

lon = -10.0638796622 #ncFile.variables['rlat'][0]
lat = 21.9878287568 #ncFile.variables['rlon'][0]

print("lon: " + str(lon) + " lat: " + str(lat))

latLon = toRot(lon, lat)

print("rlon: " + str(latLon.item(0, 0)) + " rlat: " + str(latLon.item(1,0)))

latLon = toReg(latLon.item(0, 0), latLon.item(1, 0))

print("lon: " + str(latLon.item(0, 0)) + "lat: " + str(latLon.item(1,0)))


