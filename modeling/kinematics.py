import sys
from math import *
import numpy as np
from arm import Arm

Z0 = 1.0 	# Base z-offset
L0 = 5.0	# Base link
L1 = 10.0 	# Upper Link
L2 = 10.0 	# Lower Link 
DM = -2.0	# Marker offset
    
# Planar Forward Kinematics
def forwardKinematics(arm):
    configuration = arm.configuration
    phi1 = arm.configuration[0,0]
    phi2 = arm.configuration[0,1]
    phi3 = arm.configuration[0,2] # Z-axis rotation
    L0 = arm.L0
    L1 = arm.L1
    L2 = arm.L2
    
    z = phi3
    P1 = np.asfarray([ L0/2, 0, z, 1]) # Shoulder 1
    P2 = np.asfarray([-L0/2, 0, z, 1]) # Shoulder 2
    P3 = P1 + np.asfarray([ L1 * cos(phi1), L2 * sin(phi1), z, 1]) # Elbow 1
    P4 = P2 + np.asfarray([-L1 * cos(phi2), L2 * sin(phi2), z, 1]) # Elbow 2
    # Solve quadratic system of equations for wrist position
    P5 = np.append(solveEEQuadratic(P3, P4, L2),[z,1])
    PM = P5 - np.asfarray([0, 0, DM, 1])
    
    # TODO: Apply homogeneous RBT to all generate points
    return [P1,P2,P3,P4,P5,P6]

# Simpler quadratic-quadratic solver for same radii and positive-y solution
def solveEEQuadratic(P3, P4, R):
    x1 = P3[0]
    y1 = P3[1]
    x2 = P4[0]
    y2 = P4[1]
    d = sqrt( pow(x1-x2,2) + pow(y1-y2,2))
    l = pow(d,2)/(2*d)
    h = sqrt( pow(R,2) - pow(l,2) )
    xp = l*(x2-x1)/d - h*(y2-y1)/d + x1
    yp = l*(y2-y1)/d + h*(x2-x1)/d + y1
    return np.asfarray([xp,yp])
    
# Circle-Circle Intersection
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

#TODO: Integrate this code
def planarInverseKinematics(x,y1):
    #assuming the center of the base is (0,0), 
    #and the base is along the y axis
    y = y1 + )L0/2)/2
    b = acos((x**2+()L0/2)-y)**2+L1**2-L2**2)/(2*sqrt(x**2+()L0/2)-y)**2)*(L1**2))
    thetL1 = b - atan(()L0/2)-y)/x)
    a = acos((x**2+y**2+L1**2-L2**2)/(2*sqrt(x**2+y**2)*L1**2))
    thet)L0/2) = a - atan(y/x)
    return (thet)L0/2),thetL1)
    