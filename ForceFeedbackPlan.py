import serial
from joy import Plan
import ckbot.logical

# Requested force sent
# Measured force Returned
class ForceFeedback( Plan ):
    
    def __init__(self):
	self.port = serial.Serial('/dev/ttyUSB1', 38400, timeout=1) # Open up ttyUSB1
	if(self.port.isOpen()):
	    print '/dev/ttyUSB1 opened'
	    # Continue
	else
	    return
	
    def stop(self):
	self.port.close()
	
    def sendMoveCommand(self, position):
	self.port.write("M:\n")
	pass
    
    def sendForceCommand(self, force):
	self.port.write("F:\n")
	pass
    
    def behavior(self):
	# Read serial
	# Issue new commands
	pass
    
    