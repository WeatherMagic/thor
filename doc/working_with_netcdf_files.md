# Working with NetCDF files

The following example will extract data from a NetCDF file:

- Variables consists of arrays, with the number of dimensions defined by the variable attribute. For example, the air/ta variable has three dimensions - time, lat, lon. 
- The time is an array with numbers that represent the number of days from the date specified within DIMENSION ATTRIBUTES.
- Each position in the array of the air temperature maps to the same index in the time array, meaning time[i] is the date for air[i][rlong][rlat]


```python

import datetime as dt  # Python standard library datetime  module
import netCDF4 # http://code.google.com/p/netcdf4-python/
import sys

if len(sys.argv) != 2:
    print("Usage: ")
    print("    " + sys.argv[0] + "NETCDF-FILE.nc")
    sys.exit(1)

file_path = sys.argv[1]
nc_fid = netCDF4.Dataset(file_path, 'r') # Open netCDF file for reading

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
# Extract data from NetCDF file dimensions
# These dimensions are described by variable attributes
lats = nc_fid.variables['lat'][:] 
lons = nc_fid.variables['lon'][:]
time = nc_fid.variables['time'][:]
plev = nc_fid.variables['plev'][:]

#air = nc_fid.variables['taLEVEL'][:] # Exchange LEVEL with info from file (for example ta500 or tas)
# three dimensional array
# airt[time][longitude][latitude]


``

