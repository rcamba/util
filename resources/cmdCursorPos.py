from win32api import SetCursorPos
from win32gui import GetWindowText, IsWindowEnabled, EnumWindows, GetWindowRect
from win32process import GetWindowThreadProcessId
from psutil import Process, get_pid_list
from pywintypes import error as winTypeError
from root import get_hwnds_for_pid
from sys import argv


def get_CMD_HWND():
	
	cmd_PID=-1
	cmdHwnd=-1
	
	pidList=get_pid_list()
	
	for i in range(0,len(pidList)):
		process=Process(pidList[i])
		if(process.name=="cmd.exe"):
			cmd_PID=process.pid
			break
	
	if(cmd_PID!=-1):
		hwndList=get_hwnds_for_pid(cmd_PID)
	
		
		cmdHwnd=hwndList[0]
		
		if(len(hwndList)>1):
			print "WARNING: More than one instance of cmd.exe found. Centered only first cmd.exe"
	
	else:
		print "cmd.exe not found"	
	
	return cmdHwnd
		
def centerCMD():
	"""Sets cursor to center of CMD"""
	cmdHwnd=get_CMD_HWND()
	
	try:
		rect=GetWindowRect(cmdHwnd)
		xStart = rect[0]
		yStart = rect[1]
		width = rect[2] - xStart
		height = rect[3] - yStart

		x=(width/2)+xStart
		y=(height/2)+yStart

		SetCursorPos([x,y])
	
	except winTypeError:	
		print "cmdHwnd not found"
		
	

if __name__ == '__main__':
    
	
	
	if(len(argv)==1):
		centerCMD()
		
	else:
		if(len(argv)==2):
			x=int(argv[1].split(',')[0])
			y=int(argv[1].split(',')[1])
		elif(len(argv)==3):
			x=int(argv[1])
			y=int(argv[2])
		
		SetCursorPos([x,y])
	
	
	