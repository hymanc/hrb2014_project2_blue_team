from math import *
import numpy as np
from arm import Arm
from paper import Paper
from interpolator import *

class DeltaController(object):
    def __init__(self, arm, paper):
	self.arm = arm
	self.paper = paper # Idealized paper estimate
	pass
    
    def computeError(self):
	pass
    
    def generateTrajectory(self,strokes):
	# Loop over each stroke pair
	current = self.arm.configuration
	configurations = []
	for stroke in strokes:
	    wp1 = stroke[0] # Start point of stroke
	    wp2 = stroke[1] # End point of stroke
	    # Check if current location is current waypoint (i.e. don't lift off)
	    #currentHover = np.copy(self.arm.configuration)	# Set hover over curret point
	    currentHover = np.asfarray([current[0], current[1], current[2] + 2-0])
	    print 'Current:',self.arm.configuration, currentHover
	    target1 = self.paper.paperToWorld(wp1) 	# Compute world coordinates of target
	    target2 = self.paper.paperToWorld(wp2) 	# Compute world coordinates of endpoint
	    print 'WORLD PTS:',target1,target2
	    config1 = self.arm.fullIK(target1) 		# Perform full IK on 1st target
	    config1Hover = config1 + np.asfarray([0,0,-20])	# Hover configuration over 1st target
	    config1Hover[2] = config1Hover[2] - 20	# Set height to hover
	    config2 = self.arm.fullIK(target2) 		# Perform full IK on 2nd target
	    
	    print 'Configs:', str(config1), str(config1Hover), str(currentHover)
	    current = current.reshape((3,))
	    currentHover = currentHover.reshape((3,))
	    config1Hover = config1Hover.reshape((3,))
	    config1 = config1.reshape((3,))
	    config2 = config2.reshape((3,))
	    print 'CONFIG2\n' , str(config2)
	    curHoverPts = interpolateLinear(current, currentHover, 10)
	    current = config2
	    configurations = configurations + [currentHover, config1Hover, config1, config2]
	    
	    configurations = configurations + interpolateLinear(currentHover, config1Hover, 50)
	    configurations = configurations + interpolateLinear(config1Hover, config1, 10)
	    configurations = configurations + interpolateLinear(config1, config2, 50)
	    
	return configurations
	    
