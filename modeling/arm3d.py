# Arm 3D Plot
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 3D Arm Line-Plot
class ArmPlot(Axes3D):
    def __init__(self):
	self.fig = plt.figure()
	self.ax = self.fig.add_subplot(111, projection='3d')