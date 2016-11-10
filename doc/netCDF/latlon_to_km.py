#!/usr/bin/env python3

import math
import numpy
import sys

def getDistanceFromLatLonInKm(lat1,lon1,lat2,lon2):
  R = 6371 # Radius of the earth in km
  dLat = numpy.radians(lat2-lat1)
  dLon = numpy.radians(lon2-lon1)
  a =\
    numpy.sin(dLat/2) * numpy.sin(dLat/2) +\
    numpy.cos(numpy.radians(lat1)) * numpy.cos(numpy.radians(lat2)) *\
    numpy.sin(dLon/2) * numpy.sin(dLon/2)

  c = 2 * numpy.arctan2(math.sqrt(a), math.sqrt(1-a))
  d = R * c # Distance in km
  return d



if __name__ == "__main__":

    if (len(sys.argv) != 5):
        print("Usage: ")
        print("     " + sys.argv[0] + "lon1 lat1 lon2 lat2")
        sys.exit(1)

    lon1 = float(sys.argv[1])
    lat1 = float(sys.argv[2])
    lon2 = float(sys.argv[3])
    lat2 = float(sys.argv[4])

    print("km: " + str(getDistanceFromLatLonInKm(lat1, lon1, lat2, lon2)))
