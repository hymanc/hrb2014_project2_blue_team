import numpy as np
from math import *

import ckbot.logical

class ArmDraw(JoyApp):
    
    def __init__(self):
	JoyApp.__init__( self, confPath="$/cfg/JoyApp.yml") 
	self.waypoints
	
    def onStart(self):
	# Populate servos
	self.c = ckbot.logical.Cluster()
	self.c.populate(3,{ 0x03 : 'L', 0x04 : 'R', 0x0B : 'Z'})
	
    def onEvent(self , evt):
	pass
    
    def setLeft(self, theta):
	self.c.at.L.set_position(theta)
    
    def setRight(self, theta):
	self.c.at.R.set_position(theta)

    def setZ(self, z):
	self.c.at.Z.set_position(theta)
    
    # Read in strokes from file
    def readStrokes(self, filename):
	strokes = []
	f = open(filename, 'r')
	# TODO: Read in tuples
	return strokes
    
def main():
    arm = ArmDraw()
    
    # TODO: Read in strokes from text file
    pass

if __name__ == "__main__":
    main()