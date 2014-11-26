from math import *
import numpy as np
from kinematics import *
from interpolator import *
from arm3d import *
from arm import Arm
import matplotlib as plt

# "2.5D" Delta Arm discrete time kinematics simulation
class ArmSim(object):
    
    def __init__(self):
	self.arm = Arm()	# TODO: Initialze arm object
	self.paper = Paper()	# TODO: Initialize paper object
	self.armPlot = ArmPlot('Arm') # Initialize the 3D plot
	self.paperPlot = PaperPlot()
	self.forcePlot = ForcePlot()
    
    # Run the simulation
    def run(self, waypoints, initialConfig, maxStep):
	current = initialConfig	# Current configuration
	
	# Loop over waypoints
	for i in range(0,len(waypoints)):
	    ikConfig = inverseKinematics()# Compute IK
	    nsteps = 1000 #TODO: Compute variable nsteps
	    configs = interpolateLinear(current, ikConfig, nsteps)  # Interpolate trajectory
	    # Loop over interpolated configurations
	    for k in range(0, nsteps):
		self.arm.setConfiguration(configs[:,k]) # Update arm position
		self.armPlot(self.arm, self.paper) 	# Plot
		self.armPlot.clear()
	    current = ikConfig
    
    # Round the configuration to RX64 angles
    def rx64RoundConfig(config):
	nbits = 10
	rx64Range = 5*pi/3
	if(len(config.shape) == 1):
	    config = np.reshape(config,(len(config),1)) # Reshape
	roundedConfig = np.zeros(config.shape)
	for i in range(0, config.shape[0]):
	    for j in range(0, config.shape[1])):
		binValue = round((config[i][j]/rx64Range)*pow(2,nbits))
		roundedConfig[i][j] = binValue
	return roundedConfig
	    
	    