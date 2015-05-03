

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
	
	#givenTime in seconds
	
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
	"""Opens hibLog.log and appends date and time to the file"""
	from root import hibLog
	from time import strftime, localtime
	f=open(hibLog,"a")
	t=localtime()
	s=" ".join([str(strftime("%B/%d/%Y\t %H:%M", t)),"\n"])
	f.write(s)
	f.close()

def main(setTime):	
	
	"""
	Sets program to sleep for setTime minutes
	Log is created after sleep
	Calls toDoList for ready viewing once system resumes from hibernation 
	Sets the computer to hibernate
	"""
	
	for i in range(int(setTime), 0, -1 ):
		output="Time remaining until hibernation: "+ str( i)
		loadingSplash(60, output)
	
	
	createLog()
	hibernate()
	
def hibernate():
	from toDoList import viewToDoList
	viewToDoList()
	system(r"C:\Windows\System32\rundll32.exe PowrProf.dll,SetSuspendState")#hibernate
	
if __name__ == "__main__":
	from sys import argv
	from os import system
	from ctypes import windll
	windll.kernel32.SetConsoleCtrlHandler(0, 1)
	if(len(argv)<2):
		print "Missing time parameter"
	else:
		try:
			main(int(argv[1]))
			
		except ValueError:
			errorAlert("Argument must be an integer")
		