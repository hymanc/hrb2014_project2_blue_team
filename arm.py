from math import *
import numpy as np
from kinematics import Rrpy, solveEEQuadratic

# Arm class
class Arm(object):
    def __init__(self, H):
	if(H == None):
	    self.H = np.identity(3)
	else:
	    self.H = H
	self.configuration = np.zeros((3,1))
	self.configuration[:,0] = np.asfarray([pi/4,pi/4,0])
	self.L0 = L0 #
	self.L1 = L1 #
	self.L2 = L2 # 
	self.Z0 = Z0 #
	self.ZM = ZM #
	
    # Set the current arm configuration
    def setConfiguration(self, configuration):
	self.configuration[:,0] = np.asfarray(configuration)
	
    # Set the calibration homography
    def setCalibration(self, calH):
	self.H = calH
	
    # Arm forward kinematics in robot planar frame
    def forwardKinematics(self, configuration=None):
	if(configuration == None):
	    configuration = self.configuration # Use current config if not specified
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
	'''
	P0 = np.dot(self.hbase, P0)
	P1 = np.dot(self.hbase, P1)
	P2 = np.dot(self.hbase, P2)
	P3 = np.dot(self.hbase, P3)
	P4 = np.dot(self.hbase, P4)
	P5 = np.dot(self.hbase, P5)
	P6 = np.dot(self.hbase, P6)
	'''
	#print P0,P1,P2,P3,P4,P5,P6
	return [P0,P1,P2,P3,P4,P5,P6]

    # Full 3D "IK"
    ''''
    def fullInverseKinematics(self, target):
	print 'IK Target:', str(target)
	if(target != None):
	    print 'Target', str(target)
	    target = np.asfarray(target)
	    targetRFrame = np.dot(np.linalg.inv(self.hbase), target) # Convert target to arm frame
	    print 'IK RFrame Target', str(targetRFrame)
	    planar_config = self.planarInverseKinematics(targetRFrame[0:2])
	    z = self.Z0 - target[2]
	    return np.append(planar_config, [z])
    '''
    
    # Planar IK Solver
    def planarInverseKinematics(self, planeTarget):
	# 
	planeTarget = np.asfarray(planeTarget)
	planeTarget = planeTarget[0:2]
	print 'Plane Target', str(planeTarget)
	LS = np.asfarray([-self.L0/2,0])
	RS = np.asfarray([self.L0/2,0])
	L0 = self.L0
	L1 = self.L1
	L2 = self.L2

	# Get target relative to both shoulders
	LD = planeTarget-LS
	RD = planeTarget-RS
	lld = np.linalg.norm(LD)
	lrd = np.linalg.norm(RD)
	
	# Compute resulting angles using Law of Cosines
	la = (-L2**2 + L1**2 + lrd**2)/(2*L1*lrd)
	ra = (-L2**2 + L1**2 + lld**2)/(2*L1*lld)
	if(abs(la) <= 1 and abs(ra) <= 1):
	    phi1 = atan2(RD[1],RD[0]) - acos(la)
	    phi2 = pi - atan2(LD[1],LD[0]) - acos(ra)
	else:
	    print 'Invalid Position, no IK Solution'
	    return
	return (phi1, phi2)
	
    # Get EE Position (maximally extended)
    def eePosition(self, configuration=None):
	if(configuration != None):
	    self.setConfiguration(configuration)
	pts = self.forwardKinematics()
	return pts[len(pts)-1]

    # Print arm EE Position
    def printEEPosition(self, configuration=None):
	eePos = eePosition(configuration)
	print 'EE Position:', np.around(eePos[0:3],2)
	
    # Gets the location of critical points on the arm
    def getPoints(self, configuration=None):
	if(configuration != None):
	    self.setConfiguration(configuration)
	pts = self.forwardKinematics()
	ground = [pts[0][0],pts[0][1],0]
	return {'ground': ground, 'base': pts[0], 'rshoulder': pts[1], 'lshoulder': pts[2], 'relbow': pts[3], 'lelbow': pts[4], 'wrist': pts[5], 'ee': pts[6]}
    
    # Generates a linear trajectory in paper coordinates between two points
    def generateLinearTrajectory(self, startPt, endPt, npts):
	configs = []
	startPt = np.asfarray(startPt)
	endPt = np.asfarray(endPt)
	delta = (endPt - startPt)/npts
	# Convert to 2D homogeneous
	delta = np.append(delta[0:2],[0])
	sp = np.append(startPt[0:2],[1])
	for i in range(npts):
	    pti = sp + i * delta 			# Compute intermediate paper point
	    pti = np.dot(self.homography, pti) 		# Use homography to convert to arm x-y projection coordinates
	    cfgi = self.planarInverseKinematics(pti)	# Generate IK solution
	    if(cfgi != None):
		configs.append(cfgi)			# Add new configuration (if not null)
	    
	