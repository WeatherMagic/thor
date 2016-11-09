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

#print(" -------------- GLOBAL ATTRIBUTES  ")
## Get all attributes of file
#attributes = nc_file.ncattrs()
## Print attributes
#for attribute in attributes:
#    print(attribute + ": " + repr(nc_file.getncattr(attribute)))
#    # Repr converts objects to a string representation
#print("")
#
#print(" -------------- VARIABLE ATTRIBUTES")
#for var in nc_file.variables:
#    print("Name: " + var)
#    print("Dimensions: ", nc_file.variables[var].dimensions)
#    print("Size: ", nc_file.variables[var].size) # Can't print touple
#    print("")
#
#print(" -------------- DIMENSION ATTRIBUTES")
## Gets available dimensions in file, which is a dict
#dimensions = nc_file.dimensions
## This prints all dimensions and info
#for dim in dimensions:
#    print("Name: " + dim)
#    print("Size: " + str(len(dimensions[dim])))
#
#    try:
#        print("Datatype:", repr(nc_file.variables[dim].dtype))
#        for netcdf_attribute in nc_file.variables[dim].ncattrs(): # Throws error
#            print('%s:' % netcdf_attribute, repr(nc_file.variables[dim].getncattr(netcdf_attribute)))
#        print("")
#    except KeyError:
#        # If variable doesn't exist within the netCDF file, error is thrown so catch it
#        print("Dimension " + dim + " does not have a description!")
#        print("")
#
## Extract data from NetCDF file dimensions
## These dimensions are described by variable attributes
lons = nc_file.variables['lon'][:]
rlons = nc_file.variables['rlon'][:]

lats = nc_file.variables['lat'][:]
rlats = nc_file.variables['rlat'][:]

print("Lon: " + str(lons[0]))

#print(lons[1][0])

#print(lons[len(lons)-1][len(lons[len(lons)])-1])
#print(lons[len(lons)-1][0])
#print(lons[409][423])
#print(lons[0][423])

# X wise is second, Y-wise is first

#air = nc_file.variables['taLEVEL'][:] #Exchange level with info from file
# three dimensional array

