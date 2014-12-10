import numpy as np
from math import *
from homography import *

from joy import Plan
import ckbot.logical

PAPER_HEIGHT = 279.4 # 11 in in mm
PAPER_WIDTH = 215.9 # 8.5in in mm

class CalibratePlan( JoyApp ):
    def __init__(self):
	self.arm(H, L0, L1, L2, Z0, ZM):
	self.c = ckbot.logical.Cluster()
	self.c.populate(2, {0x0D: 'R', 0x0B : 'L'})
	self.c.at.L.go_slack()	# Set servos to go slack for calibration
	self.c.at.R.go_slack()
    
    # Print to file
    def saveToFile(self):
	# Open file
	# Print calibration homography to file
	pass
    
    # Event handler
    def onEvent(self , evt):
	pass # TODO: Get space key press and increase pts
	# TODO: Get enter key press
    
# Main calibration routine
def main():
    calPlan = CalibratePlan()
    kpts = []
    opts = []
    ocfg = []
    raw_input("Bottom Left Corner\n")
    kpts.append(np.asfarray([0,0]))
    ocfg.append(np.asfarray([self.c.at.R.get_pos(), self.c.at.L.get_pos()])) # Get config
    # Compute EE Position from FK
    
    raw_input("Center of Left Edge\n")
    kpts.append(np.asfarray([0,PAPER_HEIGHT/2.0]))
    
    raw_input("Upper Left Corner\n")
    kpts.append(np.asfarray([0,PAPER_HEIGHT]))
    
    raw_input("Center of Upper Edge\n")
    kpts.append(np.asfarray([PAPER_WIDTH/2.0,PAPER_HEIGHT]))
    
    raw_input("Upper Right Corner\n")
    kpts.append(np.asfarray([PAPER_WIDTH,PAPER_HEIGHT]))
    
    raw_input("Center of Right Edge\n")
    kpts.append(np.asfarray([PAPER_WIDTH,PAPER_HEIGHT/2.0]))
    
    raw_input("Lower Right Corner\n")
    kpts.append(np.asfarray([PAPER_WIDTH,0]))
    
    print "Computing Homography"
    H = homography(kpts, opts)
    raw_input("Save homography:?  (filename): ")
    
    
    

if __name__ == "__main()__":
    main()