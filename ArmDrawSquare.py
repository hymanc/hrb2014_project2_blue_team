import numpy as np
from math import *
import ast
import ckbot.logical
from ArmMotionPlan import ArmPlan

SQUARE_SIDE = 101.6 # 4in in mm
PAPER_HEIGHT = 279.4 # 11 in in mm
PAPER_WIDTH = 215.9 # 8.5in in mm
# Top Level Arm Drawing Class
class ArmDraw(JoyApp):
    
    # 
    def __init__(self, strokeFile):
	JoyApp.__init__( self, confPath="$/cfg/JoyApp.yml") 
	self.strokes = readStrokes(strokeFile)
	
    # App startup
    def onStart(self):
	# Populate servos
	self.armPlan = ArmPlan(0x0D,0x0B) 
	
    # Event handler
    def onEvent(self , evt):
	pass
    
    # Read in strokes from file
    def readStrokes(self, filename):
	strokes = []
	f = open(filename)
	lines = f.readlines()
	for line in lines:
	    strokes = strokes + ast.literal_eval(line)
	return strokes
    
# Main
# TODO
def main():
    strokeFile = ""
    arm = ArmDraw(strokeFile)
    
    # TODO: Read in strokes from text file
    pass

if __name__ == "__main__":
    main()