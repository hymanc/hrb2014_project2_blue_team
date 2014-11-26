# Arm 3D Plot
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from kinematics import *

# 3D Arm Line-Plot
class ArmPlot(object):
    # name: Plot name
    # points: Time series of vertices to plot
    def __init__(self):
	self.fig = plt.figure()
	# 3D Subplot
	self.ax3d = self.fig.add_subplot(2, 2, 4, projection='3d')
	plt.title('3D ARM!')
	#XY, XZ, YZ Subplots
	self.axy = self.fig.add_subplot(2, 2, 1)
	plt.title('XY Plane')
	self.axz = self.fig.add_subplot(2, 2, 2)
	plt.title('XZ Plane')
	self.ayz = self.fig.add_subplot(2, 2, 3)
	plt.title('YZ Plane')
	
    # Plots the arm in 3D Space
    def plotArm(self, arm):
	pts = arm.getPoints()# Get Body Points
	self.ax3d.plot(pts['ground'], pts['base'])
	self.ax3d.plot(pts['base'], pts['lshoulder'])
	self.ax3d.plot(pts['base'], pts['rshoulder'])
	self.ax3d.plot(pts['lshoulder'], pts['lelbow'])
	self.ax3d.plot(pts['lelbow'], pts['wrist'])
	self.ax3d.plot(pts['rshoulder'], pts['relbow'])
	self.ax3d.plot(pts['relbow'], pts['wrist'])
	self.ax3d.plot(pts['wrist'], pts['marker']) # TODO: Replace with compressed marker
	plt.show()
	
    # Plot paper surface on 3D plot
    def plotPaper(self, paper):
	print 'Plotting paper'
	x = paper.corners[0,:]
	y = paper.corners[1,:]
	z = paper.corners[2,:]
	self.ax3d.plot_trisurf(x,y,z,cmap=cm.jet,linewidth=0.2)# Surface Plot
	plt.show()
	
    # Clear figure
    def clear(self):
	plt.figure(self.fig)
	plt.clf()
	
	