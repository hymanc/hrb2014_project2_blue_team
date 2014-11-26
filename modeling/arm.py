from math import *
import numpy as np

from kinematics import *

# NOTE: All measurements are in mm

# Arm class
class Arm(object):
    def __init__(self, baseOrigin, armOrientation, L0, L1, L2, Z0, ZM):
	self.baseOrigin = np.asfarray(baseOrigin)
	self.armOrientation = np.asfarray(armOrientation)
	self.configuration = np.asfarray([0,0,0])
	self.L0 = L0
	self.L1 = L1
	self.L2 = L2
	self.Z0 = Z0
	self.ZM = ZM
	
	# Generate base RBT
	
    # Set the current arm configuration
    def setConfiguration(self, configuration):
	self.configuration[:,0] = np.asfarray(configuration)
	
    # Get EE Position (maximally extended)
    def eePosition(self, configuration):
	if(configuration != None):
	    self.setConfiguration(configuration)
	pts = forwardKinematics(self)
	return pts[len(pts)-1]

    # Gets the location of critical points on the arm
    def getPoints(self, configuration):
	if(configuration != None):
	    self.setConfiguration(configuration)
	pts = forwardKinematics(self)
	ground = pts[0]
	ground[2] = 0 # Set z to 0 for ground intersection
	return {'ground': ground, 'base': pts[0], 'rshoulder': pts[1], 'lshoulder': pts[2], 'relbow': pts[3], 'lelbow': pts[4], 'wrist': pts[5], 'ee': pts[6]}