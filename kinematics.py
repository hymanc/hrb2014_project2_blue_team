# Kinematics utilities for the parallel-manipulator
import sys
from math import *
import numpy as np

Z0 = 1.0 	# Base z-offset
L0 = 5.0	# Base link
L1 = 10.0 	# Upper Link
L2 = 10.0 	# Lower Link 
DM = -2.0	# Marker offset

# Simpler quadratic-quadratic solver for same radii and positive-y solution
def solveEEQuadratic(P3, P4, R):
    x1 = P3[0]
    y1 = P3[1]
    x2 = P4[0]
    y2 = P4[1]
    d = sqrt( pow(x1-x2,2) + pow(y1-y2,2))
    l = pow(d,2)/(2*d)
    h = sqrt( pow(R,2) - pow(l,2) )
    xp = l*(x2-x1)/d + h*(y2-y1)/d + x1
    yp = l*(y2-y1)/d - h*(x2-x1)/d + y1
    return np.asfarray([xp,yp])
    
# Circle-Circle Intersection solver
def circleIntersection(center1, center2, r1, r2):
    x1 = center1[0]
    y1 = center1[1]
    x2 = center2[0]
    y2 = center2[1]
    d = sqrt( pow(x1-x2, 2) + pow(y1-y2,2) )
    l = ( pow(r1,2) - pow(r2,2) + pow(d,2))/(2*d)
    h = sqrt( pow(r1,2) - pow(l,2) )
    xp = l*(x2-x1)/d + h*(y2-y1)/d + x1
    yp = l*(y2-y1)/d - h*(x2-x1)/d + y1
    xn = l*(x2-x1)/d - h*(y2-y1)/d + x1
    yn = l*(y2-y1)/d + h*(x2-x1)/d + y1
    return [(xp,yp),(xm,ym)]

# X-axis rotation matrix
def Rx(theta):
    c = cos(theta)
    s = sin(theta)
    return np.asfarray([[1,0,0],[0,c,-s],[0,s,c]])
  
# Y-axis rotation matrix
def Ry(theta):
    c = cos(theta)
    s = sin(theta)
    return np.asfarray([[c,0,s],[0,1,0],[-s,0,c]])
  
# Z-axis rotation matrix
def Rz(theta):
    c = cos(theta)
    s = sin(theta)
    return np.asfarray([[c,-s,0],[s,c,0],[0,0,1]])

# Roll-pitch-yaw rotation matrix
def Rrpy(thetaR, thetaP, thetaY):
    return np.dot(Rz(thetaY), np.dot(Ry(thetaP), Rx(thetaR)))

# ZYZ Euler angle rotation matrix
def Rzyz(tz1, ty, tz2):
    return np.dot(Rz(tz2), np.dot(Ry(ty), Rz(tz1) ) )
    