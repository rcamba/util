from mouseMacro import slide, getpos
from math import pi
currPos=getpos()
x=100
while x>0:
	
	slide((currPos[0]**2) *pi+x , (currPos[1]**2) *pi+x)
	x=x-1
	
	print x
