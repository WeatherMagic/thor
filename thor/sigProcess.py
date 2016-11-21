#!/usr/bin/env python3

import numpy as np
import scipy.interpolate
import numpy.matlib


# -------------------------------------
def interpolate(climateData,
                returnDimension):

    maxAxis = climateData.shape

    removedDimensions = []
    dimensions = 3

    for maxAxe, retDim in zip(maxAxis, returnDimension):
        if maxAxe == 1 and retDim > 1:
                return({"ok": False,
                        "error":
                        "Singular dimension is to be\
                        interpolated, can't do that."})

    # Checking dimensionality of requested data
    if maxAxis[0] == 1:
        dimensions -= 1
        removedDimensions.append("time")
    if maxAxis[1] == 1:
        dimensions -= 1
        removedDimensions.append("long")
    if maxAxis[2] == 1:
        dimensions -= 1
        removedDimensions.append("lat")

    # Depending on dimensionality in data do appropriate interpolation
    interpolDim = []
    newMaxAxis = []

    if "time" not in removedDimensions:
        interpolDim.append(returnDimension[0])
        newMaxAxis.append(maxAxis[0])
    if "lat" not in removedDimensions:
        interpolDim.append(returnDimension[1])
        newMaxAxis.append(maxAxis[1])
    if "long" not in removedDimensions:
        interpolDim.append(returnDimension[2])
        newMaxAxis.append(maxAxis[2])

    if dimensions > 1:
        interpolData = np.squeeze(interpolateFunc(np.squeeze(climateData),
                                                  newMaxAxis,
                                                  interpolDim))
    else:
        return({"ok": False,
                "errorMessage":
                "Data less then 2d please increase search area"})

    if dimensions < 3:
        return({"ok": True,
                "data": interpolData})

    return({"ok": True,
            "data": interpolData})


# -------------------------------------
def interpolateFunc(climateData,
                    maxAxis,
                    returnDimension):

    # Coordinates to the climateData
    grid = []
    interpolGrid = []

    for axis, dimensions in zip(maxAxis, returnDimension):
        grid.append(np.linspace(0, axis-1, axis))
        interpolGrid.append(np.linspace(0, axis-1, dimensions))

    weatherInterpolationFunc = scipy.interpolate.RegularGridInterpolator(
        grid,
        climateData)

    interPoints = pointsFromGrid(interpolGrid)

    # Interpolate data for the 3D points created earlier
    return weatherInterpolationFunc(interPoints).reshape(returnDimension)


# -------------------------------------
def pointsFromGrid(gridList):
    dim = len(gridList)

    if dim == 3:
        meshGrid = np.meshgrid(gridList[0],
                               gridList[1],
                               gridList[2],
                               indexing='ij')
    elif dim == 2:
        meshGrid = np.meshgrid(gridList[0],
                               gridList[1],
                               indexing='ij')
    elif dim == 1:
        meshGrid = np.meshgrid(gridList[0],
                               indexing='ij')
    return np.vstack(meshGrid).reshape(dim, -1).T
