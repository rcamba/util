from root import getPixel, get_hwnds_for_pid, getProcessPID
from setProcessPriority import changeProcPriority
from psutil import get_pid_list, Process
from win32com import client
from win32gui import GetWindowRect
from time import sleep
from string import lower
from msvcrt import kbhit, getch
from mouseMacro import move

def soundRecordActive():
	result=False
	
	processList=get_pid_list()
	
	for PID in processList:
		
		if lower(Process(PID).name)=="soundrecorder.exe":
			result=True
			break
			
	return result
	
def checkForColorChange(rect):
	
	go=True
	print "Watching."
	while go:
		
		if (kbhit()):
			if (ord(getch())!=54):#if keypress is not '6' end loop
				go=False
		
		
		if getPixel(rect[0]+230,rect[1]+50) != DEFAULT_COLOR:
		
			shell.SendKeys("6")
			sleep(0.1)
			if kbhit():
				getch()
		
		sleep(1)#prevents error from getPixel checking too often
	
	
if __name__ == "__main__":
	
	DEFAULT_COLOR=(200,200,201)
	
	shell=client.Dispatch("WScript.Shell")
	if soundRecordActive():
		
		changeProcPriority("soundRecorder","low")
		
		handleList=get_hwnds_for_pid(getProcessPID("soundRecorder"))
		recorderHwnd=handleList[2]
		rect=GetWindowRect(recorderHwnd)#third hwnd from list
		
		checkForColorChange(rect)
	else:
		print "Sound recorder isn't active. Terminating script."