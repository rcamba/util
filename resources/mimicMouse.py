#mimicMouse
# get change in mouse
from mouseMacro import getpos
from time import sleep

origPos=getpos()
while(1):
	g=getpos()
	changeX=abs( origPos[0]- g[0])
	changeY=abs( origPos[1]- g[1])
	print changeX, changeY
	#sleep(1)