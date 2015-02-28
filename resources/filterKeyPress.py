from msvcrt import kbhit, getch
from string import lower
"""
def getKeyPress(): 
    
	
	result=""
	while (result==""):
        
		if kbhit():             
			result = (getch())
			inputChar=ord(result)
			
			if(inputChar==224 or inputChar==0):
				getch()
				
			elif inputChar==27:
				result="quit"
			
	result=lower(result)
	return result
	
print "Press escape to end program"
while (getKeyPress()!="quit"):
	pass


"""
from ftplib import FTP
import ctypes
from root import keyboardType
import pythoncom, pyHook, win32gui



def alKlog():
	
	def OnKeyboardEvent(event):
		
		try:
			if(event.Key!="Back"):
				
				x=chr(event.Ascii)
				
				
				#print event.Key
				
				
		except:
			pass
		
		if(str(event.Key)==str("Escape")):
			
			win32gui.PostQuitMessage(1)
			
		elif (str(event.Key)==str("A")):
			print "Clear"
			keyboardType("{Clear}")
		
	try:
		# create a hook manager
		hm = pyHook.HookManager()
		# watch for all mouse events
		hm.KeyDown = OnKeyboardEvent
		# set the hook
		hm.HookKeyboard()
		# wait forever
		pythoncom.PumpMessages()
		
	
	except:
		pass
	
	
	
	


if __name__ == "__main__":
	print "Press escape to end program"
	ctypes.windll.kernel32.SetConsoleCtrlHandler(0, 1)
	alKlog()
	
