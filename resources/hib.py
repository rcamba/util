r"""
Sets the computer to hibernate after x amount of minutes and logs the time and date of hibernation
-x is a required parameter from the user
-x can be 0
-x can't be negative
-Name of log file is "hibLog.txt"

TO DO:
	Add a way to cancel/add more time without having to kill and call hib.bat
	Check if vlc task exists before ending task to prevent killing non-existant tasks
"""


def loadingSplash(givenTime, output="", splash=['.', "..", "..."]):
	from sys import stdout
	from time import sleep, time
	
	def writeSlashB(string):
		result=""
		for i in range(0,len(string)):
			result=result+"\b"
		stdout.write(result)	

	def clearOut(string):
		clear=""
		for i in range(0,len(string)):
			clear=clear+" "
		stdout.write(clear)
		
		return clear

	i=0	
	stdout.write(output)
	startTime=time()
	while (time()-startTime) < givenTime :
		
		
		splashText=splash[i]
		stdout.write(splashText)
		sleep(0.5)
		stdout.flush()
		
		writeSlashB(splashText)
		
		i=i+1
		if(i==len(splash)):
			writeSlashB(clearOut(splashText))
			i=0
			
	stdout.flush()
	
	writeSlashB(output)

def createLog():
	"""Opens hibLog.txt and appends date and time to the file"""
	from root import hibLog
	from time import strftime, localtime
	f=open(hibLog,"a")
	t=localtime()
	s=" ".join([str(strftime("%B/%d/%Y\t %H:%M", t)),"\n"])
	f.write(s)
	f.close()

def hibernate(setTime):	
	from root import killProcess
	"""Sets program to sleep for setTime minutes
	
	Log is created after sleep
	Kills vlc 
	Calls toDoList for ready viewing once system resumes from hibernation 
	Sets the computer to hibernate
	"""
	
	for i in range(int(setTime), 0, -1 ):
		#print "Time remaining until hibernation: ", i
		#time.sleep( 60 )
		output="Time remaining until hibernation: "+ str( i)
		loadingSplash(60, output)
	
	
	createLog()
		
	killProcess("vlc")
	system("start cmd /c \"tdl & pause\"")
	system("C:/Users/Kevin/Desktop/force_hib.lnk")
	
	
if __name__ == "__main__":
	from sys import argv
	from os import system
	from ctypes import windll
	windll.kernel32.SetConsoleCtrlHandler(0, 1)
	if(len(argv)<2):
		print "Missing time parameter"
	else:
		if(float(argv[1]) > -1 ):
			hibernate(float(argv[1]))
		else:
			print "Invalid parameter. Time cannot be a negative value"