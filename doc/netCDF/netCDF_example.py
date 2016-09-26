#!/usr/bin/env python3

import datetime as dt  # Python standard library datetime  module
import netCDF4 # Import netCDF
import sys

# Check if an argument is given
if len(sys.argv) != 2:
    print("Usage: ")
    print("    " + sys.argv[0] + "NETCDF-FILE.nc")
    sys.exit(1)

# Read argument (filename)
file_path = sys.argv[1]
nc_file = netCDF4.Dataset(file_path, 'r') # Open netCDF file for reading

print(" -------------- GLOBAL ATTRIBUTES  ")
# Get all attributes of file
attributes = nc_file.ncattrs()
# Print attributes
for attribute in attributes:
    print(attribute + ": " + repr(nc_file.getncattr(attribute)))
    # Repr converts objects to a string representation
print("")

print(" -------------- DIMENSION ATTRIBUTES")
# Gets available dimensions in file, which is a dict
dimensions = nc_file.dimensions
# This prints all dimensions and info
for dim in dimensions:
    print("Name: " + dim)
    print("Size: " + str(len(dimensions[dim])))
    
    try:
        print("Datatype:", repr(nc_file.variables[dim].dtype))
        for netcdf_attribute in nc_file.variables[dim].ncattrs(): # Throws error
            print('%s:' % netcdf_attribute, repr(nc_file.variables[dim].getncattr(netcdf_attribute)))
        print("")
    except KeyError:
        # If variable doesn't exist within the netCDF file, error is thrown so catch it
        print("Dimension " + dim + " does not have a description!")
        print("")

# Extract data from NetCDF file dimensions
# These dimensions are described by variable attributes
lats = nc_file.variables['lat'][:] 
lons = nc_file.variables['lon'][:]
time = nc_file.variables['time'][:]
plev = nc_file.variables['plev'][:]

#air = nc_file.variables['taLEVEL'][:] #Exchange level with info from file
# three dimensional array
# airt[time][longitude][latitude]

