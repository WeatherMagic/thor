# Working with NetCDF files

The following example will extract data from a NetCDF file:

Variables consists of arrays, with the number of dimensions defined by the variable attribute. For example, the air/ta variable has three dimensions - time, lat, long

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
# air[time][longitude][latitude]

plev = nc_fid.variables['plev'][:]

``

