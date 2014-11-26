from math import *
import numpy as np
from kinematics import Rrpy

# A paper model
class Paper(object):
    X_SIZE = 215.9	# Paper x-size in mm (8.5in)
    Y_SIZE = 279.4	# Paper y-size in mm (11in)
    
    # Paper constructor (not made from construction paper)
    # normalRotation (roll, pitch, yaw angles) of normal vector from [0,0,1]
    def __init__(self, rbt):
	#self.origin = np.asfarray(origin)
	# Determine rigid body transform to paper origin
	self.paperFrame = rbt
	self.hInv = np.linalg.inv(self.paperFrame)
	#self.paperFrame = np.identity(4)
	#self.paperFrame[0:3,3] = self.origin # Set translation
	#R = Rrpy(normalRotation[0], normalRotation[1], normalRotation[2]) # Set rotation
	#self.paperFrame[0:3,0:3] = R
	
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
  
    # Gets the world coordinates of a 2D point on the paper
    def paperToWorld(self, paperPt):
	paperPt = np.asfarray(paperPt)
	if(paperPt.shape[0] == 2):	# Convert to homogeneous
	    paperPt = np.append(paperPt, [0.0,1.0])
	elif(paperPt.shape[0] == 3):
	    paperPt = np.append(paperPt, [1.0])
	worldPt = np.dot(self.paperFrame, paperPt) # Apply RBT
	return worldPt
	
    # Gets the paper coordinates of a world point
    def worldToPaper(self, worldPt):
	worldPt = np.asfarray(worldPt)
	if(worldPt.shape[0] == 2):
	    worldPt = np.append(worldPt, [1.0])
	paperPt = np.dot(self.hInv, worldPt)
	return paperPt
	
    # Get an indexed corner of the paper
    def getCorner(self, index):
	if(index > 0 and index < 4):
	    return self.corners[:,index]
	
    # Check if a line segment between two points intersects the paper
    # TODO: Finish this
    # @return Point of intersection on paper plane
    def intersection(self, p1, p2):
	# Convert points into paper frame
	p1p = np.dot(self.hInv, p1)
	p2p = np.dot(self.hInv, p2)
	# Check if z-signs are opposite
	if((p2p[2] >= 0 and p1p[2] < 0) or (p2p[2] < 0 and p1p[2] >= 0)):
	    # Find intersection at zp = 0
	    #[ax+by+cz=d]
	    print 'Unbounded Plane intersection'