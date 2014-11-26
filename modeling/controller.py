from math import *
import numpy as np
from arm import Arm
from paper import Paper

class DeltaController(object):
    def __init__(self, arm, paper):
	self.arm = arm
	self.paper = paper # Idealized paper estimate
	pass
    
    def computeError(self):
	pass
    
    def generateTrajectory(self,strokes):
	# Loop over each stroke pair
	configurations = []
	for stroke in strokes:
	    wp1 = stroke[0] # Start point of stroke
	    wp2 = stroke[1] # End point of stroke
	    # Check if current location is current waypoint (i.e. don't lift off)
	    currentHover = np.copy(self.arm.configuration)	# Set hover over curret point
	    currentHover[2] = currentHover[2] + 20
	    target1 = self.paper.paperToWorld(wp1) 	# Compute world coordinates of target
	    target2 = self.paper.paperToWorld(wp2) 	# Compute world coordinates of endpoint
	    print 'WORLD PTS:',target1,target2
	    config1 = self.arm.fullIK(target1) 		# Perform full IK on 1st target
	    config1Hover = np.copy(config1)		# Hover configuration over 1st target
	    config1Hover[2] = config1Hover[2] + 20	# Set height to hover
	    config2 = self.arm.fullIK(target2) 		# Perform full IK on 2nd target
	    configurations.append(interpolateLinear(self.arm.configuration, currentHover, 100))
	    configurations.append(interpolateLinear(currentHover, config1Hover, 500))
	    configurations.append(interpolateLinear(config1Hover, config1, 100))
	    configurations.append(interpolateLinear(config1, config2, 500))
	return configurations
	    
