# Plot of strokes on paper
from math import *
import numpy as np
import matplotlib.pyplot as plt
from paper import Paper

class ForcePlot(object):
    def __init__(self):
	self.fig = plt.figure()
	self.aforce = self.fig.add_subplot(1,2,2)
	plt.title('Contact Force')
	plt.xlabel('Time (s)')
	plt.ylabel('Force (N)')
	plt.show()
	
    def plot(self, forcePoints):
	self.aforce.plot(forcePoints)
	plt.show()
	
    def clear(self):
	figure(self.fig)
	plt.clf()