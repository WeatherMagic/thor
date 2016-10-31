#!/usr/bin/env python3

from numpy import *


def getRotationMatrix(axis, degrees):
    """
    Input: 
        Rotation axis, angle to rotate
    Output: 
        Rotation matrix (3x3)
    """
    angle = radians(degrees)
    Ux = axis[0]
    Uy = axis[1]
    Uz = axis[2]
    
    cosT = cos(angle)
    sinT = sin(angle)
    oneMinC = 1-cosT

    rotMat = matrix(array([
        [cosT+Ux*Ux*oneMinC, Ux*Uy*oneMinC-Uz*sinT, Ux*Uz*oneMinC+Uy*sinT],
        [Uy*Ux*oneMinC+Uz*sinT, cosT+Uy*Uy*oneMinC, Uy*Uz*oneMinC-Ux*sinT],
        [Uz*Ux*oneMinC-Uy*sinT, Uz*Uy*oneMinC+Ux*sinT, cosT+Uz*Uz*oneMinC]
        ]))

    return rotMat


def lonLatToCart(lonLat):
    """
    Input: 
        Lon,lat as numpy matrix
    Output:
        Cartesian coordinates, denoting earth radius as 1 unit
    """
    lon = radians(lonLat.item((0,0)))
    lat = radians(lonLat.item((1,0)))
    
    xCoord = sin(lon)*cos(lat)
    # yCoord is upwards, computer graphics style
    yCoord = sin(lat)
    # zCoord is "towards the observer", computer graphics style
    zCoord = cos(lon)*cos(lat)

    return matrix(array([[xCoord], [yCoord], [zCoord]]))


def cartToLonLat(cart):
    """
    Input: 
        Carthesian coordinates as numpy matrix
    Output:
        Lon,lat as numpy matrix
    """
    xCoord = cart.item((0,0))
    yCoord = cart.item((1,0))
    zCoord = cart.item((2,0))
 
    lon = 0
    epsilon = 0.001
    if abs(zCoord) > 0+epsilon:
        lon = degrees(arctan(xCoord/zCoord))
    elif abs(yCoord) > 1-epsilon:
        lon = 0
    elif xCoord > 0:
        lon = degrees(pi/2.0)
    else:
        lon = degrees(-pi/2.0)
    
    lat = 0
    if yCoord > 1-epsilon:
        lat = degrees(pi/2.0)
    elif yCoord < -1+epsilon:
        lat = degrees(-pi/2.0)
    else:
        lat = degrees(arcsin(yCoord))

    return matrix(array([[lon], [lat]]))


def regFromRot(lon, lat):
    """
    Takes rotated coordinates and outputs regular coordinates
    """
    rotatedCoord = lonLatToCart(matrix(array([[lon], [lat]])))

    # Axises to rotate around
    xAxis = [1,0,0]
    yAxis = [0,1,0]
    # South Pole location in rotated coordinate system
    spRotLon = -162
    spRotLat = 39.25
    # How far to rotate around Y
    angleY = 0-spRotLon
    # How far to rotate around X
    angleX = 90+spRotLat
    
    # Create rotation matrixes
    Ry = getRotationMatrix(yAxis, angleY)
    Rx = getRotationMatrix(xAxis, angleX)
    
    # Get regular cart coordinates
    regCartCoord_tmp = Ry * rotatedCoord
    regCartCoord = Rx * regCartCoord_tmp
    print(regCartCoord)
    
    return cartToLonLat(regCartCoord)



