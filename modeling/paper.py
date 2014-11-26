from math import *
import numpy as np

class Paper(object):
    X_SIZE = 215.9	# Paper x-size in mm (8.5in)
    Y_SIZE = 279.4	# Paper y-size in mm (11in)
    
    # Paper constructor (not made from construction paper)
    def __init__(self, origin, normal, normalRotation):
	self.origin = np.asfarray(origin)
	self.normal = normal/np.linalg.norm(normal)
	# Determine rigid body transform to paper origin
	self.paperFrame = np.identity(4)
	self.paperFrame[0:3,3] = self.origin # Set translation
	# TODO: Set rotation
	
	# Generate paper corners
	corner1 = np.asfarray([0,0,0,1])
	corner2 = np.asfarray([X_SIZE, 0, 0,1])
	corner3 = np.asfarray([X_SIZE, Y_SIZE, 0,1])
	corner4 = np.asfarray([0, Y_SIZE, 0,1])
	self.corners = np.zeros((3,4))
	self.corners[:,0] = corner1
	self.corners[:,1] = corner2
	self.corners[:,2] = corner3
	self.corners[:,3] = corner4
	
	self.corners = np.dot(paperFrame, self.corners) # Transform corners
	
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
	
    # Return unit normal
    def paperZ(self):
	return self.normal
	
    # Check if a line segment between two points intersects the paper
    # 
    # @return Point of intersection on paper plane
    def intersection(self, p1, p2):
	# Check for basic intersection of line/plane
	    # Check for intersection point between p1, p2
		# Check for intersection between bounds of paper
	return None