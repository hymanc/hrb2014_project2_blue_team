from math import *
from numpy import *

def inverseKinematics(a1,a2,a3,x,y1):
    #a1 is the length of the base 
    #a2 is the lengths of the two upper arms
    #a3 is the lengths of the two forearms
    #assuming the center of the base is (0,0), 
    #and the base is along the y axis
    
    y = y1 + a1/2
    
    b = acos((x**2+(a1-y)**2+a2**2-a3**2)/(2*sqrt(x**2+(a1-y)**2)*(a2**2))
    
    theta2 = b - atan((a1-y)/x)
    
    a = acos((x**2+y**2+a2**2-a3**2)/(2*sqrt(x**2+y**2)*a2**2))
    
    theta1 = a - atan(y/x)
    
    return (theta1,theta2)
