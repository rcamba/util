from time import sleep




	
import sys

#containerList containts string and pctNum all as strings
def drawLoadingBar(containerList):
	
	#sys.stdout.write("\r%d%%" % pctNum)
	#sys.stdout.flush()
	
	for i in range(0,len(containerList)):
		msg=containerList[i][0] +" "+ containerList[i][1]
		sys.stdout.write(msg)
		
		
		sys.stdout.write("\b" * (len(containerList[i][0] +" "+ containerList[i][1])+3))
		sys.stdout.flush()	
		sys.stdout.write("\n")
		
		
		
		
		
		
	
	
	

if __name__=="__main__":

	for i in range(100):
		sleep(1)
		argList=[("Amaburi",str(i)+"%"), ("Uchii Kyoudai",str(i*2)+"%")]
		drawLoadingBar(argList)
		
		
		