#!/usr/bin/env python3

from numpy import *
import math


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
    lon = radians(lonLat.item((0, 0)))
    lat = radians(lonLat.item((1, 0)))

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
    xCoord = cart.item((0, 0))
    yCoord = cart.item((1, 0))
    zCoord = cart.item((2, 0))

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


def toReg(rlon, rlat):
    """
    rot2reg seams to be working
    Takes rotated coordinates and outputs regular coordinates.

    This function is ported from fortran by Gustav Strandberg from SMHI.
    This is totally un-documented - have no idea what we're doing.
    """
    # This is different from original regrot
    pxrot = -rlon
    pyrot = -rlat

    zrad = pi/180.0
    zradi = 1.0/zrad

    pycen = 39.25
    pxcen = -162

    zsycen = sin(zrad*(pycen+90.0))
    zcycen = cos(zrad*(pycen+90.0))

    zsxrot = sin(zrad*pxrot)
    zcxrot = cos(zrad*pxrot)
    zsyrot = sin(zrad*pyrot)
    zcyrot = cos(zrad*pyrot)
    zsyreg = zcycen*zsyrot+zsycen*zcyrot*zcxrot
    zsyreg = max(zsyreg,-1.0)
    zsyreg = min(zsyreg,+1.0)

    pyreg = arcsin(zsyreg)*zradi

    zcyreg = cos(pyreg*zrad)
    zcxmxc = (zcycen*zcyrot*zcxrot-zsycen*zsyrot)/zcyreg
    zcxmxc = max(zcxmxc,-1.0)
    zcxmxc = min(zcxmxc,+1.0)
    zsxmxc = zcyrot*zsxrot/zcyreg
    zxmxc  = arccos(zcxmxc)*zradi

    #gs080207
    #This is different from original regrot
    if (zsxmxc < 0.0):
        zxmxc = -zxmxc+360

    pxreg = zxmxc + pxcen

    return matrix(array([[pxreg], [pyreg]]))

def toRot(lon, lat):
    """
    reg2rot
    Takes regular coordinates and outputs rotated coordinates.

    This function is also ported by Gustav Strandberg.
    """
    pxreg = lon
    pyreg = lat

    zrad = pi/180.0
    zradi = 1.0/zrad

    pycen = 39.25
    pxcen = -162

    zsycen = sin(zrad*(pycen+90.0))
    zcycen = cos(zrad*(pycen+90.0))

    zxmxc  = zrad*(pxreg - pxcen)
    zsxmxc = sin(zxmxc)
    zcxmxc = cos(zxmxc)
    zsyreg = sin(zrad*pyreg)
    zcyreg = cos(zrad*pyreg)
    zsyrot = zcycen*zsyreg - zsycen*zcyreg*zcxmxc
    zsyrot = max(zsyrot,-1.0)
    zsyrot = min(zsyrot,+1.0)

    pyrot = arcsin(zsyrot)*zradi

    zcyrot = cos(pyrot*zrad)
    zcxrot = (zcycen*zcyreg*zcxmxc+zsycen*zsyreg)/zcyrot
    zcxrot = max(zcxrot,-1.0)
    zcxrot = min(zcxrot,+1.0)
    zsxrot = zcyreg*zsxmxc/zcyrot

    pxrot = arccos(zcxrot)*zradi

    if (zsxrot < 0.0):
        pxrot = -pxrot

    # gs080206
    # This is different from original regrot
    rlat = -pyrot
    rlon = -pxrot

    return matrix(array([[rlon], [rlat]]))




