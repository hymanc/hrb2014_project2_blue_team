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
    # Global paper location input for simulation
    PAPER_LOCATION = np.asfarray([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]])
    # Set of waypoints on paper
    #WAYPOINTS = [[(10,0),(10,30)],[[10,15],[20,15]],[[20,0],[20,30]]

    def __init__(self):
	self.arm = Arm(np.asfarray([0,-200,0]), np.asfarray([0,0,0]), 100, 160, 200, 1, -20)	# TODO: Initialze arm object
	self.paperPlot = PaperPlot()
	self.forcePlot = ForcePlot()
	self.paper = Paper(np.asfarray([0,0,0]), np.asfarray([0,-pi/2,-pi/2]))	# TODO: Initialize paper object
	self.armPlot = ArmPlot() # Initialize the 3D plot
	self.armPlot.plotPaper(self.paper)
	self.armPlot.plotArm(self.arm)
    
    # Run the simulation
    def run(self, waypoints, initialConfig, minStep=100):
	initialConfig = np.asfarray(initialConfig)
	current = initialConfig	# Current configuration
	
	# Loop over waypoints
	for i in range(0,len(waypoints)):
	    #TODO: Convert waypoints into arm frame
	    ikConfig = np.append(self.arm.planarIK(waypoints[i]),[50])# Compute IK
	    print str(ikConfig)
	    nsteps = minStep #TODO: Compute variable nsteps
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
    waypoints = [[0,200,0],[0,100,0]]
    asim.run(waypoints,[pi/2,pi/2,0])
    
if __name__ == '__main__':
    main()
    
	    