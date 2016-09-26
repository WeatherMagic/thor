# Working with NetCDF files

The example in the file netCDF_example.py will extract data from a NetCDF file. This file is aimed at discribing this a little bit more, trying to make reading the file understandable.

- Variables consists of arrays, with the number of dimensions defined by the variable attribute. For example, the air/ta variable has three dimensions - time, lat, lon. 
- The time is an array with numbers that represent the number of days from the date specified within DIMENSION ATTRIBUTES.
- Each position in the array of the air temperature maps to the same index in the time array, meaning time[i] is the date for air[i][rlong][rlat]

So to try and visualize this, here's a small example.

```

Time units, days since 2016-09-26
Time array:
[0 1 2 3 4 5 6]

rlat array:
[56 57 58 59 60 61]

rlong array:
[15 16 17 18 19 20 21 22]

Temperature is now a three dimensional array, where first dimension is time and has the same length as time, the second is rlat and the third is rlong and has the same length. In order to get air temperature in Linköping (lat 58, long 15) at tuesday 27 sept 2016 (2016-09-27):

air_temp = temp[1][2][0]


```


