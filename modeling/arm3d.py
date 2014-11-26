# Arm 3D Plot
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
# TODO: Include IK

# 3D Arm Line-Plot
class ArmPlot(object):
    # name: Plot name
    # points: Time series of vertices to plot
    def __init__(self, name):
	self.name = name
	self.fig = plt.figure()
	self.ax3d = self.fig.add_subplot(2, 2, 4, projection='3d')
	plt.title('ARM!')
	#XY, XZ, YZ subplots
	self.axy = self.fig.add_subplot(2, 2, 1)
	plt.title('XY Plane')
	self.axz = self.fig.add_subplot(2, 2, 2)
	plt.title('XZ Plane')
	self.ayz = self.fig.add_subplot(2, 2, 3)
	plt.title('YZ Plane')
	
    # Plots the arm in 3D Space
    def plot(self, arm, paper):
	# Get Body Points
	# Plot links between body points
	# Plot End effector
	plt.show()
	
    # Clear figure
    def clear(self):
	plt.figure(self.fig)
	plt.clf()
	
	