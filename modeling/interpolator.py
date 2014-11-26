from math import *
import numpy as np

# Linear vector interpolation
def interpolateLinear(c1, c2, npts):
    print 'Linearly interpolating', npts, 'points'
    print 'C1:',c1, 'C2:', c2
    c1 = np.asfarray(c1)
    c2 = np.asfarray(c2)
    pts = np.zeros((np.shape(c1)[0],npts)) # Preallocate configs
    print 'ptsSize:', pts.shape
    pts[:,0] = c1		# Assign first point
    pts[:,npts-1] = c2	# Assign last point
    delta = (c2-c1)/(npts-1) 	# Compute linear step
    for i in range(1,npts-1):	
	pts[:,i] = pts[:,i-1] + delta
    return pts
