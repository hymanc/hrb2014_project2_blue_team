from math import *
import numpy as np

from kinematics import *

# All measurements are in mm
class Arm(object):
    def __init__(self, baseOrigin, armNormal, L0, L1, L2, Z0, ZM):
	self.baseOrigin = np.asfarray(baseOrigin)
	self.armNormal = np.asfarray(armNormal)
	self.configuration = np.asfarray([0],[0],[0])
	self.L0 = L0
	self.L1 = L1
	self.L2 = L2
	self.Z0 = Z0
	self.ZM = ZM
	
    # Set the current arm configuration
    def setConfiguration(self, configuration):
	self.configuration[:,0] = np.asfarray(configuration)
