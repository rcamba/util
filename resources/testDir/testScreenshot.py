import win32gui, win32con, win32ui, win32api
from win32com import client
from time import sleep
from datetime import datetime

from os import getenv
from sys import path, argv, exit as sys_exit
path.insert(0,getenv("UtilResources"))


from root import getProcessPID


def takeScreenshot():
	
	windowsHandle = win32gui.GetDesktopWindow()

	rect=win32gui.GetWindowRect(windowsHandle)
	width=rect[2]-rect[0]
	height=rect[3]-rect[1]
	left = rect[0] #win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
	top = rect[1] #win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)

	hwindc = win32gui.GetWindowDC(windowsHandle)
	srcdc = win32ui.CreateDCFromHandle(hwindc)
	memdc = srcdc.CreateCompatibleDC()
	dataBitMap = win32ui.CreateBitmap()

	dataBitMap.CreateCompatibleBitmap(srcdc, width, height)
	memdc.SelectObject(dataBitMap)
	memdc.BitBlt((0, 0), (width, height), srcdc, (left, top), win32con.SRCCOPY)
	fileName="".join(["SS_", appName,"_", str(datetime.now().strftime("%b-%d-%Y@%H_%M_%S")).strip(), ".png"])
	print "Saved screenshot as :", fileName
	dataBitMap.SaveBitmapFile(memdc, fileName)

	srcdc.DeleteDC()
	memdc.DeleteDC()
	win32gui.ReleaseDC(windowsHandle, hwindc) 

if __name__ == "__main__":
	
	
	
	if len(argv)>1:
		appName=argv[1]
		
	else:#default
		appName="notepad++" #get name from current window in focus?
	
	
	pid=getProcessPID(appName)
	
	shell=client.Dispatch("Wscript.Shell")
	if shell.AppActivate(pid)==False:
		
		print "Error:\t"
		print appName, "is not a recognized application."
		sys_exit(1)
	
	
	else:
	
		takeScreenshot()
		
		