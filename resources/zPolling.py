#5min polling
from time import sleep
from mouseMacro import getpos
from os import system


while(1==1):
	g=getpos()
	counter=0
	while(getpos()==g):
		
		sleep(1)
		counter=counter+1
		
		if counter==300:
			system("monoff")