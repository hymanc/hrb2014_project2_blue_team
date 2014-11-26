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
	self.ax3d = self.fig.add_subplot(1, 1, 1, projection='3d')
	plt.title('3D ARM!')
	self.ax3d.set_xlim(-250,250)
	self.ax3d.set_ylim(-250,250)
	self.ax3d.set_zlim(-250,250)
	#XY, XZ, YZ Subplots
	'''
	self.axy = self.fig.add_subplot(2, 2, 1)
	plt.title('XY Plane')
	self.axz = self.fig.add_subplot(2, 2, 2)
	plt.title('XZ Plane')
	self.ayz = self.fig.add_subplot(2, 2, 3)
	plt.title('YZ Plane')
	'''
	
    # Plots the arm in 3D Space
    def plotArm(self, arm):
	pts = arm.getPoints()# Get Body Points
	
	self.plotLine(pts['ground'], pts['base'],lw=10)
	self.plotLine(pts['base'], pts['lshoulder'],lw=5)
	self.plotLine(pts['base'], pts['rshoulder'],lw=5)
	self.plotLine(pts['lshoulder'], pts['lelbow'],lw=5)
	self.plotLine(pts['lelbow'], pts['wrist'],lw=5)
	self.plotLine(pts['rshoulder'], pts['relbow'],lw=5)
	self.plotLine(pts['relbow'], pts['wrist'],lw=5)
	self.plotLine(pts['wrist'], pts['ee'],'purple') # TODO: Replace with compressed marker
	plt.gca().set_aspect('equal', adjustable='box')
	# TODO: Projections 
	plt.show()
	
    def plotLine(self, p1, p2, lineColor='b', lw=2.5):
	x = [p1[0], p2[0]]
	y = [p1[1], p2[1]]
	z = [p1[2], p2[2]]
	line = self.ax3d.plot(x,y,z)
	plt.setp(line, color=lineColor, linewidth=lw)
	
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
	
	