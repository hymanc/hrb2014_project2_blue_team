# Arm 3D Plot
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from kinematics import *
import matplotlib.animation as animation

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
	self.l = [0] * 20
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
	for i in range(0,len(self.l)):
	    print self.l[i]
	    if(self.l[i] != 0 and self.l[i] != None):
		print 'Old line available'
		#self.ax3d.lines3d.remove(self.l[i])
		self.l[i].pop(0)
		self.l[i].remove()
	
	self.l[0] = self.plotLine(pts['ground'], pts['base'],lw=10)
	self.l[1] = self.plotLine(pts['base'], pts['lshoulder'],lw=5)
	self.l[2] = self.plotLine(pts['base'], pts['rshoulder'],lw=5)
	self.l[3] = self.plotLine(pts['lshoulder'], pts['lelbow'],lw=5)
	self.l[4] = self.plotLine(pts['lelbow'], pts['wrist'],lw=5)
	self.l[5] = self.plotLine(pts['rshoulder'], pts['relbow'],lw=5)
	self.l[6] = self.plotLine(pts['relbow'], pts['wrist'],lw=5)
	self.l[7] = self.plotLine(pts['wrist'], pts['ee'],'purple') # TODO: Replace with compressed marker
	self.fig.gca().set_aspect('equal', adjustable='box')
	# TODO: Projections 
	#self.fig.show()
	return self.l
	
    def plotLine(self, p1, p2, lineColor='g', lw=2.5):
	x = [p1[0], p2[0]]
	y = [p1[1], p2[1]]
	z = [p1[2], p2[2]]
	line = self.ax3d.plot(x,y,z,'')
	plt.setp(line, color=lineColor, linewidth=lw)
	return line
    
    # Plot paper surface on 3D plot
    def plotPaper(self, paper):
	#print 'Plotting paper'
	x = paper.corners[0,:]
	y = paper.corners[1,:]
	z = paper.corners[2,:]
	
	self.paperRender = self.ax3d.plot_trisurf(x,y,z,linewidth=0.2)# Surface Plot
	self.fig.show()
	return self.paperRender

    '''
    def drawAnimation(self, arm, configurations, paper):
	arms = []
	for i in range(0,configurations.shape[1]):
	    print 'Adding plot'
	    arm.setConfiguration(configurations[:,i])
	    arms.append(self.plotArm(arm))
	self.animation = animation.FuncAnimation(self.fig, self.animationFrame, 100, fargs=(arm,paper), interval=50, blit=False)
	self.fig.show()
	
    def animationFrame(self, num, arm, paper):
	#print num
	self.plotPaper(paper)
    '''
    
    # Clear figure
    def clear(self):
	#self.fig.clf()
	pass
	