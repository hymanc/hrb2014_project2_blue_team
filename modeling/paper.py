from math import *
import numpy as np
from kinematics import Rrpy

# A paper model
class Paper(object):
    X_SIZE = 215.9	# Paper x-size in mm (8.5in)
    Y_SIZE = 279.4	# Paper y-size in mm (11in)
    
    # Paper constructor (not made from construction paper)
    # normalRotation (roll, pitch, yaw angles) of normal vector from [0,0,1]
    def __init__(self, origin, normalRotation):
	self.origin = np.asfarray(origin)
	# Determine rigid body transform to paper origin
	self.paperFrame = np.identity(4)
	self.paperFrame[0:3,3] = self.origin # Set translation
	R = Rrpy(normalRotation[0], normalRotation[1], normalRotation[2]) # Set rotation
	self.paperFrame[0:3,0:3] = R
	
	# Generate paper corners
	corner1 = np.asfarray([0, 0, 0 ,1])
	corner2 = np.asfarray([Paper.X_SIZE, 0, 0, 1])
	corner3 = np.asfarray([Paper.X_SIZE, Paper.Y_SIZE, 0, 1])
	corner4 = np.asfarray([0, Paper.Y_SIZE, 0, 1])
	tempcorners = np.zeros((4,4))
	self.corners = np.zeros((4,4))
	tempcorners[:,0] = corner1
	tempcorners[:,1] = corner2
	tempcorners[:,2] = corner3
	tempcorners[:,3] = corner4
	#print str(tempcorners)
	self.corners = np.dot(self.paperFrame, tempcorners)
	print str(self.corners)
	#print str(self.paperFrame)
    
    # Obtain paper x-axis unit vector
    def paperX(self):
	x = self.corners[:,1]-self.corners[:,0]
	x = x/np.linalg.norm(x)
	return x
    
    # Obtain paper y-axis unit vector
    def paperY(self):
	y = self.corners[:,3]-self.corners[:,0]
	y = y/np.linalg.norm(y)
	return y
	
    # Obtain paper z-axis (normal) vector
    def paperZ(self):
	return self.normal
  
    # Get an indexed corner of the paper
    def getCorner(self, index):
	if(index > 0 and index < 4):
	    return self.corners[:,index]
	
    # Check if a line segment between two points intersects the paper
    # TODO: Finish this
    # @return Point of intersection on paper plane
    def intersection(self, p1, p2):
	# Check for basic intersection of line/plane
	    # Check for intersection point between p1, p2
		# Check for intersection between bounds of paper
	return None