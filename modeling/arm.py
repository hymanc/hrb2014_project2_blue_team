from math import *
import numpy as np
from kinematics import Rrpy, solveEEQuadratic

# NOTE: All measurements are in mm

# Arm class
class Arm(object):
    def __init__(self, hbase, L0, L1, L2, Z0, ZM):
	self.hbase = hbase
	#self.baseOrigin = np.asfarray(baseOrigin)
	#self.armOrientation = np.asfarray(armOrientation)
	self.configuration = np.zeros((3,1))
	self.configuration[:,0] = np.asfarray([pi/4,pi/4,0])
	self.L0 = L0
	self.L1 = L1
	self.L2 = L2
	self.Z0 = Z0
	self.ZM = ZM
	
	#Generate base RBT
	#self.hbase = np.identity(4)
	#self.hbase[0:3,3] = self.baseOrigin
	#ang = self.armOrientation
	#self.hbase[0:3,0:3] = Rrpy(ang[0], ang[1], ang[2])
	
    # Set the current arm configuration
    def setConfiguration(self, configuration):
	self.configuration[:,0] = np.asfarray(configuration)
	
    # Arm forward kinematics
    def forwardKinematics(self):
	configuration = self.configuration
	phi1 = configuration[0]
	phi2 = configuration[1]
	phi3 = configuration[2] # Z-axis rotation
	L0 = self.L0
	L1 = self.L1
	L2 = self.L2
	DM = self.ZM
	z = (self.Z0 + phi3)[0]
		
	P0 = [0,0,z,1]
	P1 = P0 + np.asfarray([ L0/2, 0, 0, 0]) # Shoulder 1 (Right)
	P2 = P0 + np.asfarray([-L0/2, 0, 0, 0]) # Shoulder 2 (Left)
	P3 = P1 + np.asfarray([ L1 * cos(phi1), L2 * sin(phi1), 0, 0]) # Elbow 1 (Right)
	P4 = P2 + np.asfarray([-L1 * cos(phi2), L2 * sin(phi2), 0, 0]) # Elbow 2 (Left)
	# Solve quadratic system of equations for wrist position
	P5 = np.append(solveEEQuadratic(P3, P4, L2),[z,1])	# Wrist
	P6 = P5 - np.asfarray([0, 0, DM, 0]) #
	# Apply homogeneous RBT to all generate points
	P0 = np.dot(self.hbase, P0)
	P1 = np.dot(self.hbase, P1)
	P2 = np.dot(self.hbase, P2)
	P3 = np.dot(self.hbase, P3)
	P4 = np.dot(self.hbase, P4)
	P5 = np.dot(self.hbase, P5)
	P6 = np.dot(self.hbase, P6)
	#print P0,P1,P2,P3,P4,P5,P6
	return [P0,P1,P2,P3,P4,P5,P6]

    # Full 3D "IK"
    def fullIK(self, target):
	if(target != None):
	    print 'Target', str(target)
	    target = np.asfarray(target)
	    planar_config = self.planarIK(target[0:2])
	    z = self.Z0-target[2]
	    return np.append(planar_config, [z])
    
    # Planar IK Solver
    def planarIK(self, planeTarget):
	x = planeTarget[0]
	y1 = planeTarget[1]
	a1 = self.L0
	a2 = self.L1
	a3 = self.L2
	y = y1 + a1/2.0
	b = acos((x**2 + (a1 - y)**2 + a2**2 - a3**2)/(2*sqrt(x**2 + (a1 - y)**2)*(a2**2)))
	theta2 = b - atan2( (a1 - y), x )
	a = acos((x**2 + y**2 + a2**2 - a3**2)/(2*sqrt(x**2 + y**2)*a2**2))
	theta1 = a - atan2(y,x)
	return (theta1,theta2)
	
    # Get EE Position (maximally extended)
    def eePosition(self, configuration=None):
	if(configuration != None):
	    self.setConfiguration(configuration)
	pts = forwardKinematics(self)
	return pts[len(pts)-1]

    # Gets the location of critical points on the arm
    def getPoints(self, configuration=None):
	if(configuration != None):
	    self.setConfiguration(configuration)
	pts = self.forwardKinematics()
	ground = [pts[0][0],pts[0][1],0]
	return {'ground': ground, 'base': pts[0], 'rshoulder': pts[1], 'lshoulder': pts[2], 'relbow': pts[3], 'lelbow': pts[4], 'wrist': pts[5], 'ee': pts[6]}