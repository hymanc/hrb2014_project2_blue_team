# SVD Homography Estimation
# Requires 5 more more correspondence points (the more the better)
# Cody Hyman
# EECS 498: Hands on Robotics

import numpy as np
from math import *

# Computation of calibration homography from paper to arm
def homography(knownPts, obsPts):
    A = []
    if(len(knownPts) >= 5 and len(obsPts) >= 5 and len(knownPts) == len(obsPts)):
	for i in range(obsPts): # Assemble coorespondences
	    x = knownPts[i][0]
	    y = knownPts[i][1]
	    u = obsPts[i][0]
	    v = obsPts[i][1]
	    A.append([-x,-y,-1,0,0,0,u*x,u*y,u])
	    A.append([0,0,0,-x,-y,-1,v*x,v*y,v])
	A = np.asfarray(A)
	U,s,V = np.linalg.svd(A, full_matrices=True) # Compute SVD
	Umin = U[:,9] # Extract smallest singular value U
	H = Umin.reshape((3,3)) # Reshape into homography
	print 'Computed Homography\n', str(H), '\n'
	return H
    else:
	print 'Insufficient number of points
	return