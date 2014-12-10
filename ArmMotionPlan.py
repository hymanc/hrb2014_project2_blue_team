from joy import Plan
import ckbot.logical
from collections import deque
from homography import *

# 2.5-D Delta Arm Driver
class ArmPlan( Plan ):
    
    def __init__(self, rAddr, lAddr):
	self.c = ckbot.logical.Cluster()
	self.c.populate(2, { rAddr : 'R', lAddr : 'L'})
	self.pts = deque([])
	self.mode = "IDLE"
    
    def appendPoints(self, pts):
	self.pts = self.pts + pts
	
    def setConfiguration(self, config):
	if(len(config) == 3):
	    self.setRightShoulder(config[0])
	    self.setLeftShoulder(config[1])
	    self.setZ(config[2])
	else:
	    print 'Invalid configuration length'
	    
    # Convert an angle in radians to centidegrees
    def radToCentidegrees(angle):
	return int(180.0*angle/(100*pi))
	
    # Set Left Shoulder Position
    def setLeftShoulder(self, theta):
	# TODO: Check if motion is within valid range
	thetaCDeg = radToCentidegrees(theta)
	self.c.at.L.set_pos(thetaCDeg)
    
    # Set Right Shoulder Position
    def setRightShoulder(self, theta):
	# TODO: Check if motion is within valid range
	thetaCDeg = radToCentidegrees(theta)
	self.c.at.R.set_pos(thetaCDeg)
    
    # Set Z-axis height
    def setZ(self, z):
	pass
    
    # Set the motors to go slack for calibration
    def calibrateMode(self):
	self.mode = "CALIBRATE"
	self.c.at.L.go_slack()
	self.c.at.R.go_slack()
	
    def runMode(self):
	self.mode = "RUN"
    
    def idleMode(self):
	self.mode = "IDLE"
	
    # Primary behavior
    def behavior(self):
	pass
	while(True):
	    # Run mode handling
	    if(self.mode == "RUN"):
		if(len(self.pts) > 0):
		    self.setConfiguration(self.pts.popleft())
		    
	    yield self.forDuration(0.05)