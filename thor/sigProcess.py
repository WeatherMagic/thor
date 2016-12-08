#!/usr/bin/env python3

import numpy as np
import scipy.interpolate
import numpy.matlib
from enum import Enum


"""
Creates an Enum so that different axis
are always maped to a certain value
"""


class Axis(Enum):
    time = 0
    lat = 1
    long = 2

"""
Takes a 2D or 3D ndarray and checks dimensionality
and interpolates to requested dimension.
If requested dimension can't be obtained from the data or if the
data is of lower dimensionality then 2D, an error is returned.
"""


def interpolate(climateData,
                returnDimensions):

    maxAxes = climateData.shape

    removedDimensions = []
    dimensions = 3

    # Checking dimensionality of requested data
    # aborting if it is less than 2d
    for maxAxis, axis, retDim in zip(maxAxes, Axis, returnDimensions):
        if maxAxis == 1:
            dimensions -= 1
            removedDimensions.append(axis)
            if retDim > 1:
                return({"ok": False,
                        "errorMessage":
                        "Singular dimension is to be" +
                        " interpolated, can't do that."})

    # Depending on dimensionality in data do appropriate interpolation
    interpolDim = []
    newMaxAxis = []

    for axis in Axis:
        if axis not in removedDimensions:
            interpolDim.append(returnDimensions[axis.value])
            newMaxAxis.append(maxAxes[axis.value])

    if dimensions > 1:
        interpolData = np.squeeze(interpolateFunc(np.squeeze(climateData),
                                                  newMaxAxis,
                                                  interpolDim))
    else:
        return({"ok": False,
                "errorMessage":
                "Data less then 2d can't interpolate."})

    if dimensions < 3:
        return({"ok": True,
                "data": interpolData})

    return({"ok": True,
            "data": interpolData})

"""
Takes data creates a data grid and an interpolation grid
and interpolates the data to fit the interpolation grid.
"""


def interpolateFunc(climateData,
                    maxAxes,
                    returnDimension):

    # Coordinates to the climateData
    grid = []
    interpolGrid = []

    for maxAxis, dimensions in zip(maxAxes, returnDimension):
        grid.append(np.linspace(0, maxAxis-1, maxAxis))
        interpolGrid.append(np.linspace(0, maxAxis-1, dimensions))

    weatherInterpolationFunc = scipy.interpolate.RegularGridInterpolator(
        grid,
        climateData)

    interPoints = pointsFromGrid(interpolGrid)

    # Interpolate data for the 3D points created earlier
    return weatherInterpolationFunc(interPoints).reshape(returnDimension)

"""
Given a 1D, 2D or 3D grid, creates every point in that grid.
"""


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
