import serial
from joy import Plan
import ckbot.logical

# Requested force sent
# Measured force Returned
class ForceFeedback( Plan ):
    
    def __init__(self, app, *arg, **kw):
	Plan.__init__(self, app, *arg, **kw ) # Initialize Plan
	self.port = serial.Serial('/dev/ttyACM0', 115200, timeout=1) # Open up Nucleo VCP (ttyACM0)
	if(self.port.isOpen()):
	    print 'EE serial link opened'
	    # Continue
	else
	    return
	
    def stop(self):
	self.port.close()
	
    def parseForce(self, fstr):
	#"F:XXXX"
	
    def sendMoveCommand(self, position):
	self.port.write("M:\n")
	pass
    
    def sendForceCommand(self, force):
	self.port.write("F:\n")
	pass
    
    def behavior(self):
	# Read serial
	# Issue new commands
	while(True):
	    if(self.port.isOpen()):
		lines = self.port.readlines() # Read all lines
		if(len(lines) > 0):
		    fline = lines[-1]
		    # Parse Force command
	    yield self.forDuration(0.05)
    
    