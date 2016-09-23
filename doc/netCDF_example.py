#!/usr/bin/env python3

import datetime as dt  # Python standard library datetime  module
import netCDF4 # http://code.google.com/p/netcdf4-python/
import sys

if len(sys.argv) != 2:
    print("Usage: ")
    print("    " + sys.argv[0] + "NETCDF-FILE.nc")
    sys.exit(1)

file_path = sys.argv[1]
nc_fid = netCDF4.Dataset(file_path, 'r') # Open netCDF file for reading

print(" -------------- GLOBAL ATTRIBUTES  ")
# Get all attributes of file
attributes = nc_fid.ncattrs()
# Print attributes
for attribute in attributes:
    print(attribute + ": " + repr(nc_fid.getncattr(attribute)))
    # Repr converts objects to a string representation
print("")

print(" -------------- DIMENSION ATTRIBUTES")
# Gets available dimensions in file, which is a dict
dimensions = nc_fid.dimensions
# This prints all dimensions and info
for dim in dimensions:
    print("Name: " + dim)
    print("Size: " + str(len(dimensions[dim])))
    
    try:
        print("Datatype:", repr(nc_fid.variables[dim].dtype))
        for ncattr in nc_fid.variables[dim].ncattrs():
            print('%s:' % ncattr, repr(nc_fid.variables[dim].getncattr(ncattr)))
        print("")
    except KeyError:
        print("Dimension " + dim + " does not have a description!")
        print("")


print(" -------------- VARIABLE ATTRIBUTES")
for var in nc_fid.variables:
    print("Name: " + var)
    print("Dimensions: ", nc_fid.variables[var].dimensions)
    print("Size: ", nc_fid.variables[var].size) # Can't print touple
    print("")

# Extract data from NetCDF file dimensions
# These dimensions are described by variable attributes
lats = nc_fid.variables['lat'][:] 
lons = nc_fid.variables['lon'][:]
time = nc_fid.variables['time'][:]

air = nc_fid.variables['ta200'][:] # three dimensional array
# airt[time][longitude][latitude]

plev = nc_fid.variables['plev'][:]
