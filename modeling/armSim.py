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
from controller import DeltaController

# "2.5D" Delta Arm discrete time kinematics simulation
class ArmSim(object):
    # ===== Paper location input for simulation =====
    Rp = Rrpy(pi/2,0,0) # Roll-pitch-yaw rotation parameterization
    PAPER_BASE = np.identity(4)		      # Paper frame rigid body transform
    PAPER_BASE[0:3,0:3] = Rp		      # Paper rotation matrix
    PAPER_BASE[0:3,3]  = np.asfarray([-Paper.X_SIZE/2,0,0]) # Paper origin
    
    # Arm Location
    Ra = Rrpy(-pi/2-0.05,pi/2,0)		# Arm Roll-Pitch-Yaw base orientation parameterization
    ARM_BASE = np.identity(4)			# Arm fixed-base rigid body transform
    ARM_BASE[0:3,3] = np.asfarray([250,-50,0])	# Arm origin 
    ARM_BASE[0:3,0:3] = Ra			# Set rotation
		 
    INITIAL_CONFIG = np.asfarray([pi/4,pi/4,0])	# Initial arm joint configuration
    
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
	self.controller = DeltaController(self.arm, self.paper)
    
    # Run the simulation
    def run(self, strokes, initialConfig, minStep=100):
	initialConfig = np.asfarray(initialConfig)
	current = initialConfig	# Current configuration
	
	# Loop over waypoints
	#for i in range(0,len(strokes)):
	'''
	ikConfig = np.append(self.arm.planarIK(strokes[i][0]),[50])# Compute IK
	print str(ikConfig)
	nsteps = minStep
	configs = interpolateLinear(current, ikConfig, nsteps)  # Interpolate trajectory
	print configs.shape'''
	    
	configs = self.controller.generateTrajectory(strokes)
	
	# Loop over interpolated configurations
	for k in range(0, len(configs)):
	    print 'Step', k
	    print str(configs[k])
	    self.arm.setConfiguration(self.rx64RoundConfig(configs[k])) # Update arm position
	    self.armPlot.clear()
	    self.armPlot.plotArm(self.arm) 	# Plot
	    self.armPlot.plotPaper(self.paper)# Plot paper again
	    draw()
	    self.armPlot.fig.show()
	    sleep(0.001)	
	current = ikConfig
    
    # Round the configuration to RX64 angles
    def rx64RoundConfig(self, config, randomness=0):
	nbits = 10
	rx64Range = 5.0*pi/3.0
	
	dConfig = (config/rx64Range) * pow(2.0, nbits)
	print 'Discrete configuration:', str(dConfig)
	dConfig = np.round(dConfig)
	roundedConfig = dConfig/pow(2.0, nbits) * rx64Range
	print 'Rounded Configuration', str(roundedConfig)
	# TODO: Randomness
	'''
	if(len(config.shape) == 1):
	    config = np.reshape(config,(len(config),1)) # Reshape
	roundedConfig = np.zeros(config.shape)
	for i in range(0, config.shape[0]):
	    for j in range(0, config.shape[1]):
		binValue = round((config[i][j]/rx64Range)*pow(2,nbits))
		roundedConfig[i][j] = binValue
	'''
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
    
	    