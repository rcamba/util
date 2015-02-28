from win32gui import SendMessage
from win32con import HWND_BROADCAST, WM_SYSCOMMAND
from msvcrt import kbhit, getch
from time import sleep

def IsKeyPressed(): 
    
	retVal=False
	result=""
	while result=="":
		if kbhit():             
			result = (getch())
			inputChar=ord(result)
			if(inputChar==224 or inputChar==0):
				getch()
				
		sleep(0.5)
	
	if len(result)>0:
		retVal=True
	
	return retVal

def turnOffMonitor(SC_MONITORPOWER):
	SendMessage(HWND_BROADCAST, WM_SYSCOMMAND, SC_MONITORPOWER, 2)
	
def turnOnMonitor(SC_MONITORPOWER):
	SendMessage(HWND_BROADCAST, WM_SYSCOMMAND, SC_MONITORPOWER, -1)

if __name__ == "__main__":
	
	SC_MONITORPOWER = 0xF170
	#turnOffMonitor(SC_MONITORPOWER)
	
	
	SendMessage(HWND_BROADCAST, WM_SYSCOMMAND, SC_MONITORPOWER, 2)
	
	#if IsKeyPressed():
	#	turnOnMonitor(SC_MONITORPOWER)
	
	