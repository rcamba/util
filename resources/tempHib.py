from mouseMacro import rightclick, click, move
from time import sleep
from root import keyboardType
from os import system
from sys import argv
if __name__=="__main__":
	if len(argv)==1:
		cTime=30
	else:
		cTime=int(argv[1])
	for m in range(cTime,0,-1):
		print "Time remaining: ", m
		sleep(60)
	

		
	
	#system("shutdown /s")
	keyboardType("^{ESCAPE}")
	
	move(340,1010) 
	sleep(5)
	click()
	#move(420,1010) 
	#sleep(5)
	#click()
	
	
