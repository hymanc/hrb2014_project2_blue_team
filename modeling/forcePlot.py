# Plot of strokes on paper
from math import *
import numpy as np
import matplotlib.pyplot as plt
from paper import Paper

class ForcePlot(object):
    def __init__(self):
	self.fig = plt.figure()
	self.aforce = self.fig.add_subplot(1,1,1)
	plt.title('Contact Force')
	plt.xlabel('Time (s)')
	plt.ylabel('Force (N)')
	plt.show()
	
    def plot(self, forcePoints, idealPoints):
	self.aforce.plot(forcePoints)
	if(idealPoints != None):
	    self.aforce.plot(idealPoints, 'g')
	plt.show()
	
    def clear(self):
	figure(self.fig)
	plt.clf()