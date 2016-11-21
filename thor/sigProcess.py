#!/usr/bin/env python3

import numpy as np
import scipy.interpolate

# -------------------------------------
def interpolate(climateData,
                returnDimension):
    (maxTime,
     maxLat,
     maxLong) = climateData.shape

    dimensions = 3
    for dimension in returnDimension:
        if dimension == 1:
            dimensions -= 1

    if dimensions == 3:
        return interpolate3D(climateData,
                             maxTime,
                             maxLat,
                             maxLong,
                             returnDimension)
    elif dimensions == 2:
        return interpolate2D(climateData,
                             maxTime,
                             maxLat,
                             maxLong,
                             returnDimension)
    elif dimensions == 1:
        return interpolate1D(climateData,
                             maxTime,
                             maxLat,
                             maxLong,
                             returnDimension)
    else:
        return({"ok": False,
                "errorMessage":
                "Requested zero dimensional interpolation"})

# -------------------------------------
def interpolate3D(climateData,
                  maxTime,
                  maxLat,
                  maxLong,
                  returnDimension):

        # Coordinates to the climateData
        timeCoord1D = np.linspace(0, maxTime-1, maxTime)
        latCoord1D = np.linspace(0, maxLat-1, maxLat)
        longCoord1D = np.linspace(0, maxLong-1, maxLong)

        # Creares a euclidian grid from the 3 coordinate axels
        grid = (timeCoord1D,
                latCoord1D,
                longCoord1D)

        # From the climateData and coordinate axels to the data
        # RegularGridInterpolator creates an interpolation function.
        # The interpolation function outputs interpolation value for
        # a given 3D point in the grid set.
        weatherInterpolationFunc = scipy.interpolate.RegularGridInterpolator(
            grid,
            climateData)

        # Create axis (area) where we want interpolated data returned
        interTimeCoord = np.linspace(0, maxTime-1, returnDimension[0])
        interLatCoord = np.linspace(0, maxLat-1, returnDimension[1])
        interLongCoord = np.linspace(0, maxLong-1, returnDimension[2])

        # Points (3D) created from a meshgrid of the
        # interpolation coordinate axis
        # (https://se.mathworks.com/help/matlab/ref/meshgrid.html).
        # These points are wihin the area specified in former step.
        interPoints = np.vstack(np.meshgrid(
            interTimeCoord,
            interLatCoord,
            interLongCoord,
            indexing='ij')).reshape(3, -1).T

        # Interpolate data for the 3D points created earlier
        interpolatedClimateData = (weatherInterpolationFunc(
            interPoints)).reshape(returnDimension)

        return({"ok": True,
                "data": interpolatedClimateData})

# -------------------------------------
def interpolate2D(climateData,
                  maxTime,
                  maxLat,
                  maxLong,
                  returnDimension):
    return({"ok": True,
                "data": []})

# -------------------------------------
def interpolate1D(climateData,
                  maxTime,
                  maxLat,
                  maxLong,
                  returnDimension):
    return({"ok": True,
                "data": []})
