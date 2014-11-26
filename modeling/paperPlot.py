# Plot of strokes on paper
from math import *
import numpy as np
import matplotlib.pyplot as plt
from paper import Paper

class PaperPlot(object):
    def __init__(self):
	self.fig = plt.figure()
	self.adwg = self.fig.add_subplot(1,1,1)
	plt.title('Drawing')
	plt.xlabel('X (mm)')
	plt.ylabel('Y (mm)')
	plt.xlim(0,Paper.X_SIZE)
	plt.ylim(0,Paper.Y_SIZE)
	self.fig.gca().set_aspect('equal', adjustable='box')
	plt.show()
	
    # Execute the plotting
    def plot(self, drawingPoints):
	self.adwg.plot(drawingPoints)
	plt.show()
    
    # Draw ideal shape
    def drawIdeal(self, idealPoints):
	self.adwg.plot(idealPoints,'g')
	plt.show()
	
    # Erase plots
    def erase(self):
	figure(self.fig)
	plt.clf()