from math import *
import numpy as np
from kinematics import *
from interpolator import *
from arm3d import *
from paperPlot import *
from forcePlot import *
from arm import Arm
from paper import Paper
import matplotlib as plt
from time import sleep

# "2.5D" Delta Arm discrete time kinematics simulation
class ArmSim(object):
    # ===== Paper location input for simulation =====
    Rp = Rrpy(pi/2,0,0) # Roll-pitch-yaw rotation parameterization
    PAPER_BASE = np.identity(4)		      # Paper frame rigid body transform
    PAPER_BASE[0:3,0:3] = Rp		      # Paper rotation matrix
    PAPER_BASE[0:3,3]  = np.asfarray([0,0,0]) # Paper origin
    
    # Arm Location
    Ra = Rrpy(-pi/2-0.05,pi/2,0)		# Arm Roll-Pitch-Yaw base orientation parameterization
    ARM_BASE = np.identity(4)			# Arm fixed-base rigid body transform
    ARM_BASE[0:3,3] = np.asfarray([100,-100,0])	# Arm origin 
    ARM_BASE[0:3,0:3] = Ra			# Set rotation
		 
    INITIAL_CONFIG = np.asfarray([pi/2,pi/2,0])	# Initial arm joint configuration
    
   # ===== Set of waypoints on paper =====
    WAYPOINTS = [[[10,0],[10,30]],[[10,15],[20,15]],[[20,0],[20,30]]]

    def __init__(self):
	self.arm = Arm(self.ARM_BASE, 100, 160, 200, 1, -20)	# TODO: Initialze arm object
	self.paperPlot = PaperPlot()
	self.forcePlot = ForcePlot()
	self.paper = Paper(self.PAPER_BASE)	# TODO: Initialize paper object
	self.armPlot = ArmPlot() # Initialize the 3D plot
	self.armPlot.plotPaper(self.paper)
	self.armPlot.plotArm(self.arm)
    
    # Run the simulation
    def run(self, waypoints, initialConfig, minStep=100):
	initialConfig = np.asfarray(initialConfig)
	current = initialConfig	# Current configuration
	# TODO: Stroke implementation
	
	# Loop over waypoints
	for i in range(0,len(waypoints)):
	    #TODO: Convert waypoints into arm frame
	    ikConfig = np.append(self.arm.planarIK(waypoints[i][0]),[50])# Compute IK
	    print str(ikConfig)
	    nsteps = minStep
	    configs = interpolateLinear(current, ikConfig, nsteps)  # Interpolate trajectory
	    print configs.shape
	    # Loop over interpolated configurations
	    for k in range(0, nsteps):
		print 'Step', k
		self.arm.setConfiguration(configs[:,k]) # Update arm position
		#self.armPlot.fig.set(visible=0)
		self.armPlot.clear()
		self.armPlot.plotArm(self.arm) 	# Plot
		self.armPlot.plotPaper(self.paper)# Plot paper again
		draw()
		self.armPlot.fig.show()
		#self.armPlot.fig.set(visible=1)
		sleep(0.003)	
	    #self.armPlot.drawAnimation(self.arm, configs, self.paper)
	    current = ikConfig
    
    # Round the configuration to RX64 angles
    def rx64RoundConfig(config):
	nbits = 10
	rx64Range = 5*pi/3
	if(len(config.shape) == 1):
	    config = np.reshape(config,(len(config),1)) # Reshape
	roundedConfig = np.zeros(config.shape)
	for i in range(0, config.shape[0]):
	    for j in range(0, config.shape[1]):
		binValue = round((config[i][j]/rx64Range)*pow(2,nbits))
		roundedConfig[i][j] = binValue
	return roundedConfig
	    
	    
# Main arm simulation
def main():
    print 'Starting arm simulation'
    asim = ArmSim()
    #waypoints = [[0,200,0],[0,100,0]]
    #asim.run(waypoints,[pi/2,pi/2,0])
    asim.run(ArmSim.WAYPOINTS,ArmSim.INITIAL_CONFIG)
    
if __name__ == '__main__':
    main()
    
	    