"""
Contains all constants and some utility methods
"""
#Directories; %username% 
animedDir="C:\\Users\\Kevin\\Util\\Resources\\animedir.txt"
musicDir="C:\\Users\\Kevin\\Music\\ytcon"
screeningDir="C:\\Users\\Kevin\\Music\\ytcon\\screen"
picDir=""
gifsDir=""
rageComicsDir=""
verticalDir=""
webComicsDir=""
showListDir=""
backUpDir="C:\\Users\\Kevin\\backUp"
garbageBin="C:\\Users\\Kevin\\usrGarbageBin"
ytAMVDir="C:\\Users\\Kevin\\Videos\\ytAMV"
ytDownloadsDir="C:\\Users\\Kevin\\Videos\\ytVids"
ytAnShows="C:\\Users\\\Kevin\\Videos\\ytAnShows"

#Files
sVLC_PID=r"C:\Users\Kevin\Util\resources\sVLC_PID"
songLogFile=r"C:\Users\Kevin\Util\resources\unitTests\prandomSongsLog.txt"
removedFilesLog="C:\\Users\\Kevin\\Util\\resources\\removedFilesLog.txt"
hibLog="C:\\Users\\Kevin\\Util\\resources\\hibLog.txt"
tagFile="C:\\Users\\Kevin\\Util\\resources\\tagFile.txt"
newestFile="C:\\Users\\Kevin\\Util\\resources\\tempDir\\newestFile.txt"#DEPRECATED since use of clipboard
vlcTitleFile="C:\\Users\\Kevin\\Util\\resources\\vlcTitleFile.txt"#DEPRECATED since use of clipboard
matrixFile="C:\\Users\\Kevin\\Util\\resources\\matrixFile.txt"
deletedTagFile="C:\\Users\\Kevin\\Util\\resources\\deletedTagFiles.txt"
quickLaunchFile="C:\\Users\\Kevin\\Util\\resources\\directoryQ.txt"
downloadedTorFiles="C:\\Users\\Kevin\\Util\\resources\\downloadedAnimeTorrents.txt"
recSearchFile="C:\\Users\\Kevin\\Util\\resources\\topFileList.txt"
toDoListTextFile="C:\\Users\\Kevin\\Util\\resources\\toDoListFile.txt"
prevDirFile="C:\\Users\\Kevin\\Util\\resources\\prevDir.txt"
downloadTorBackLog="C:\\Users\\Kevin\\Util\\resources\\downloadTorBackLog.txt"


#Variables
CMD_HEIGHT=50
PRINT_BORDER= "------------------------------"
MAX_WAIT_TIME=30 #seconds

#Utility methods
def reverseSlash(string,targetSlash):
	result=""
	if(targetSlash=="\\"):
		result=string.replace("/","\\")
		
	elif(targetSlash=="/"):
		result=string.replace("\\","/")
	
	else:
		print "Invalid target slash"
	
	return result

def compareLists(list1, list2, similar=True):
	"""
	Deletes differences between list1 and list2
	"""
	list=[]
	
	
	if(similar==True):
		for i in range(0, len(list1)):
			if(list1[i] in list2):
				list.append(list1[i])
	else:
		for i in range(len(list1)-1,-1,-1):
			if(list1[i] not in list2):
				list.append(list1[i])
		
	
	return list
	
def inSwitchList(targSwitch, switchList):
	result=False
	
	for switch in switchList:
		if targSwitch in switch:
			result=True
			break
			
	return result
		
	

def switchBoard(args, validSwitches=[]):
	from string import lower
	from inspect import stack, getmodule, getmodulename
	from sys import exit as sys_exit
	if(len(validSwitches)==0):
		
		try:
			frame=stack()[1]
			module=getmodule(frame[0]).__file__
			importFile=getmodulename(module)
			validSwitches=__import__(importFile).__dict__.get("AVAILABLE_SWITCHES")
			#AVAILABLE SWITCHES CAN'T BE INSIDE "If __name__==__main__" BLOCK
			
			if validSwitches==None:
				print "No valid switches found. Terminating script."
				sys_exit(1)
			
		except TypeError:
			print "Module of ", frame[0], " not found"
			sys_exit(1)
		
		except AttributeError:
			validSwitches=[arg.replace("-","") for arg in args]
		
	switchList=[]
	if(type(args)==list):
		
		for i in range(len(args)-1,-1,-1):

			if("-" in args[i][0]):
				switch=args[i].replace("-","")
				if(len(switch)>0):
					
					if(":" in switch):
						token=switch.split(":")
						if token[0] in validSwitches:
							switchList.append( (token[0], token[1]) )
						else:
							print token[0], ": not a valid switch"
							sys_exit(1)
						
					
					elif(lower(switch) in validSwitches ):
						switchList.append(lower(switch))
					else:
						print "Invalid switch: ", switch
						print "Terminating script."
						sys_exit(1)
				args.remove(args[i])
		
		
		#standard/ normalize slashes for file accesses
			elif("/" in args[i]):
				args[i]=args[i].replace("/","\\")
		
	else:
		print "Not a list"
	
	
	return switchList

def switchParser(args,validSwitches=[]):#returns dict, will replace switchBoard
	from inspect import stack, getmodule, getmodulename
	from sys import exit as sys_exit
	
	if(len(validSwitches)==0):
		try:
			frame=stack()[1]
			module=getmodule(frame[0]).__file__
			importFile=getmodulename(module)
			validSwitches=__import__(importFile).__dict__.get("AVAILABLE_SWITCHES")
			#AVAILABLE SWITCHES CAN'T BE INSIDE "If __name__==__main__" BLOCK
			
			if validSwitches==None:
				print "No valid switches found. Terminating script."
				sys_exit(1)
			
		except TypeError:
			print "Module of ", frame[0], " not found"
			sys_exit(1)
		
		except AttributeError:
			validSwitches=[arg.replace("-","") for arg in args]
	
	#
	switchDict={}
	for arg in args[:]:
		if arg[0]=='-':
			
			token=arg.split(':')
			
			if token[0][1:] in validSwitches:
				if len(token)==1:
					switchDict[token[0][1:]]=''
				
				elif len(token)==2:
					switchDict[token[0][1:]]=token[1]
					
				else:
					switchDict[token[0][1:]]=" ".join([ token[1:] ] )
					
			else:
				print "\nInvalid switch: ", token[0][1:]
				print "Valid switches: ", validSwitches
				exit(1)
			
			args.remove(arg)
	
	return switchDict

def listFromPiped():
	pass#get list from piped printNumberedList/ printList
	
def printList(list, endRange=-1):#(list, pretty="on",noPrint=False,endRange=-1)
#pretty is for colors+numbering  and "++,--,etc." , noPrint is just returning the str to print and no actual "print" command inside
	printNumberedList(list,endRange)

def printNumberedList(list,endRange=-1):
	
	from msvcrt import kbhit, getch
	from sys import stdout
	
	if(endRange==-1):
		endRange=len(list)
	charID="plus"
	
	print PRINT_BORDER
	origConsoleColor=getConsoleColor()
	try:
		for i in range(0,endRange):
			
			
			if( i % 2 == 0):
				setConsoleColor(3)
				
			else:
				setConsoleColor(6)
			
			if(charID=="plus"):
				print "[+",(i+1),"+]", (list[i]), "[++]"
				charID="minus"
			
			elif(charID=="minus"):	
				print "[-",(i+1),"-]", (list[i]), "[--]"
				charID="star"
			
			elif(charID=="star"):
				print "[!",(i+1),"!]", (list[i]), "[!!]"
				charID="plus"
			
				
				
			if(((i+1)%(CMD_HEIGHT))==0):
				stdout.write( "Press any key to continue" )
				if(kbhit()==False):
					inputChar=ord(getch())
					if(inputChar==224 or inputChar==0):
						getch()
					
					
					stdout.write(len("Press any key to continue")*"\b")
					
	except KeyboardInterrupt:
		setConsoleColor(origConsoleColor)
	
	finally:
		setConsoleColor(origConsoleColor)
	print PRINT_BORDER
	
def cen():
	from cmdCursorPos import centerCMD
	from threading import Thread
	Thread(target=centerCMD).start()

#add prompt as argument similar to raw_input(prompt), overwrite default prompt
#support for mulitple choices?
def chooseFromList(list, centering=True, noInvalidResult=False):
	return chooseFromNumberedList(list, centering, noInvalidResult)
	
def chooseFromNumberedList(list, centering=True, noInvalidResult=False):
	
	if(centering==True):
		cen()
	
	result=-1
	if(len(list)>1):
		print "Enter number of desired result: ", 
		try:
			choice= raw_input()
		except EOFError:#pipes
			choice=getInputFromKeyPress()
		
		
		if(choice.isdigit() and int(choice)<=len(list) and int(choice)>0):
			result=int(choice)-1
		elif noInvalidResult==True:
			result=choice
			
		else:
			print "Invalid choice. Choice was not a valid number."
	
	elif(len(list)==1):
		result=0
	
	else:
		errorAlert( "Error: Empty list." )
	
	return list[result]
	
def pipedList(stdinOutput):
	from re import findall
	from string import replace
	try:
		stdinOutput=stdinOutput.replace(PRINT_BORDER,'')
		
		pipedList=findall("\".+\"",stdinOutput)
		#print pipedList
		finalList= [x.replace('\"','') for x in pipedList]
		#print pipedList
	except Exception, e:
		errorAlert( str(e) )
		pipedList=[]
		
	return finalList

def setClipboardData(data):
	
	from win32clipboard import OpenClipboard, EmptyClipboard, SetClipboardData, CloseClipboard
	from win32con import CF_TEXT
	OpenClipboard()
	EmptyClipboard()
	SetClipboardData(CF_TEXT, data)
	CloseClipboard()

def getClipboardData():
	
	from win32clipboard import OpenClipboard, CloseClipboard, GetClipboardData
	from win32con import CF_TEXT
	OpenClipboard()
	data=GetClipboardData(CF_TEXT)
	CloseClipboard()
	
	return data

def standardizeFile(filePath):
	"""Cast to string, replace forward slash with backslash, lower string"""
	from string import lower
	return lower( str(filePath).replace('/','\\').strip() )
	
def standardizeString(targetString):
	"""Cast to string, strip string, lower string """
	from string import lower
	return lower( str(targetString).strip() )
	
def addMember(originalObject, function="", manAttrib=""):
	
	#function must contain a function call that can be applied to originalObject
	
	class Metamorph:	
		
		def __init__(self, originalObject, function):
			self.object=originalObject
			
			if(len(manAttrib)>0):
				self.attribute=manAttrib
			elif(len(function.__name__)>0):
				try:
					self.attribute=function(originalObject)
				except:
					self.attribute=None
					print "Failed to set", function, "for: ", originalObject
					raise WindowsError#TODO: CREATE OWN ERROR EXCEPTION
			else:
				print "Missing function or manual attribute parameter."
				
			
		def getObject(self):
			return self.object
		
		def getAttribute(self):
			return self.attribute
			
	
	result=Metamorph(originalObject,function)
	
	return result

def getAllPageLinks(url):	
	
	import urllib2
	user_agent = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.63 Safari/534.3'
	headers = { 'User-Agent' : user_agent }
	req = urllib2.Request(url, None, headers)
	response = urllib2.urlopen(req)
	url = response.read()
		
	
	from bs4 import BeautifulSoup, SoupStrainer
	resultsList=BeautifulSoup(url, parse_only=SoupStrainer('a'))
	resultsList=resultsList.findAll('a')
	
	return resultsList
	
def prompt(cwd=""):
	"""
	from sys import stdout
	from os import getcwd
	
	if(len(cwd)==0):
		stdout.write(str(getcwd()))
	else:
		stdout.write(cwd)
	
	
	stdout.write("\n>>>")
	"""
	from sys import stdout
	from os import system
	system("echo %CD%")
	stdout.write(">>>")
	
	
def keyPressInput(promptStr=""):
	
	if(len(promptStr)>0):
		print promptStr
	"""
	Gets input from keypress until enter is pressed.
	Tries to emulates raw_input() ; insert/overwrite always on
	For use with pipes
	"""
	
	def clear(length=1):
		stdout.write("\b"*length) #stdout cursor move back by length
		stdout.write(" "*length) #display clearing of character(s)
		stdout.write("\b"*length) #get rid of " " moving cursor forward
	
	from msvcrt import kbhit, getch
	from sys import stdout
	from os import getenv
	
	
	userInput=""
	result=[]
	cursorPos=0
	
	while(userInput!=13):
		charG=getch()
		userInput= ord(charG)
		
		if userInput==13:
			clear(len("".join(result)))
			stdout.write( "".join(result)+"\n")
			
		elif userInput==8:
			if len(result) >0 and cursorPos<=len(result) :
				clear(len(result))
				cursorPos-=1
				result.pop( "".join(result).rindex( result[cursorPos] ) )
				
				stdout.write( "".join(result) )
				stdout.write( "\b"* (len(result)-cursorPos) )
				
				
		elif userInput==224:
			userInput=ord(getch())
			
			if userInput==75: #left
				cursorPos-=1
				stdout.write("\b")
				
				
			elif userInput==77: #right
				if cursorPos < len(result):
					stdout.write(result[cursorPos])
				else:
					stdout.write(" ")
				cursorPos+=1
				
				
			elif userInput==119: #ctrl+home
				clear(len(result))
				
				result=result[cursorPos:]
				
				stdout.write("".join(result)) #let cursor remain at end
				cursorPos=len(result)
				
			elif userInput==117: #ctrl+end
				clear(len(result))
				result=result[:cursorPos]
				
				stdout.write("".join(result))
				cursorPos=len(result)
				
			elif userInput==115: #ctrl+left
				
				
				diffPos=cursorPos-"".join(result).rindex( " " )
				stdout.write("\b"*diffPos)
				cursorPos=cursorPos-diffPos
				
				
			elif userInput==116:#ctrl + right
				pass
			
		else:
			
			stdout.write(charG)
			result.insert(cursorPos,charG)
			cursorPos+=1
			

		
		
	return "".join(result)

def fileSearch(target, write=True):
	from string import lower
	from threading import Thread
	from os import system
	'''
	from os import listdir,path
	
	def recursiveWrite():#currently not being used
		nonDirList=[]
		directories=["C:\\Users\\Kevin"]
		i=len(directories)-1
		
		while(i>=0):
			holder=directories[i]
			
			try:
				fileList=listdir(holder)
			except:
				pass
			for j in range(0,len(fileList)):
				fullPath="".join([holder,"\\",fileList[j]])
				if(path.isdir(fullPath) and (fullPath not in __EXCLUDE_FOLDERS) ):
					directories.insert(0,fullPath)
				else:
					nonDirList.append(fullPath)
					writer.write(fullPath)
					writer.write("\n")
			
			directories.remove(holder)
			i=len(directories)-1
			
		writer.close()
		
	def recursiveWrite2(topLevel="C:\\Users\\Kevin"):#currently not being used
		
		traverseList=[]
		currDirContents=""
		
		try:
			currDirContents=listdir(str(topLevel))
		except WindowsError:
			pass#print "Invalid topLevel path:", topLevel
		
		for i in range(0,len(currDirContents)):
			fullPath="".join([topLevel,"\\",currDirContents[i]])
			
			if(len(fullPath)>0):
				writer.write(fullPath)
				writer.write("\n")
			
			if(path.isdir(fullPath) and (fullPath not in __EXCLUDE_FOLDERS) ):
				traverseList.append(fullPath)
				
		for i in range(0,len(traverseList)):
			recursiveWrite2(traverseList[i])
			#Thread(target=recursiveWrite2, args=(str(traverseList[i]),)).start()
			
	'''	
	
	
	resultsList=[]
	if len(target)>0:
		
		
		fileList=open(recSearchFile).read().split("\n")
		
		for i in xrange(0,len(fileList)):
			if(lower(target.strip()) in lower(fileList[i])):
				resultsList.append(fileList[i])
	
	
	#This block is all for recursiveWrite
	if write==True:
		
		command="".join("start /B %UtilResources%/iterWriteFiles.py")
		Thread(target=system, args=(command,)).start()
	
		
	return resultsList
	
def handleFileList(fList):#from fileSearch

	if(len(fList)>1):
		printNumberedList(fList)
		choice=chooseFromNumberedList(fList)
		result="".join(["\"",str(fList[choice]),"\""])
		setClipboardData(result)
	
	elif(len(fList)==0):
		result=-1
	
	else:
		result="".join(["\"",fList[0],"\""])
		setClipboardData(result)
		
	return result
	
def createBackUp(fileName):#backup before opening/writing to txt files
	from shutil import copy2
	from os import mkdir, path, rename, chdir, getcwd
	from datetime import datetime
	from time import sleep, time
	originalDir=getcwd()
	
	if(path.exists(fileName) and path.isdir(fileName)==False):
		
		timeFormat="%b-%d-%Y@%H_%M_%f"
		extension=path.splitext(fileName)[1]
		slicedFileName=path.splitext( path.split(fileName)[1] )[0]#cuts extension and path from filename
		
		dirName="".join([backUpDir,"\\",slicedFileName])
		if(path.isdir(dirName)==False):
			print "Creating new directory: ", dirName
			mkdir(dirName)
		
		datedFileName="".join([ slicedFileName,"@",str(datetime.now().strftime(timeFormat)),extension ])
		
		try:		
			copy2(fileName,dirName)
			
		except IOError:
			print "Error, cannot access directory or directory is invalid."
		
		
		chdir(dirName)
		
		if(getcwd()==dirName):
			winError=None #/lock?
			timeCounter=0
			initTime=time()
			while winError==None and timeCounter<MAX_WAIT_TIME:
				try:
					datedFileName="".join([ slicedFileName,"@",str(datetime.now().strftime(timeFormat)),extension ])
					rename( str(path.split(fileName)[1]), datedFileName)
					
					winError="clear"
				except:
					timeCounter=time()-initTime
					#print "Failed to rename ", str(path.split(fileName)[1]), " to ", datedFileName
					
				
		
	else:
		print fileName ," is not a valid file."
	
	if(getcwd()!=originalDir):
		chdir(originalDir)

def killProcess(processName="", pid=-1):
	from psutil import get_pid_list, Process, error
	from os import kill
	from signal import SIGILL
	from string import lower
	
	if(len(processName)>0 or pid!=-1):
		
		success=-1
		
		if(processName.isdigit()):
			pid=int(processName)
			kill(pid, SIGILL)
			success=1
		
		elif(pid==-1):
			if(".exe" not in processName):
				processName=".".join([lower(processName),"exe"])
			for procPID in get_pid_list():
				try:
					if lower(Process(procPID).name)==processName:
						kill(procPID, SIGILL)
						success=1
						
				except error.NoSuchProcess:
					pass
			
			
		else:
			print "Unable to find process."
	else:
		print "Missing processName or pid parameter"
	
	return success

def getPixel(x=-1,y=-1):
	"""
		Returns RGB of given x and y location. 
		If no arguments given then default location will be current mouse position
	"""
	
	from win32gui import GetDesktopWindow, GetWindowDC, GetPixel
	from win32api import GetCursorPos
	from sys import exit as sys_exit
	
	if(x==-1 and y==-1):
		x=GetCursorPos()[0]
		y=GetCursorPos()[1]
	
	
	if(x!=-1 and y!=-1):
		i_desktop_window_id = GetDesktopWindow()
		i_desktop_window_dc = GetWindowDC(i_desktop_window_id)#device context
		try:
			long_colour = GetPixel(i_desktop_window_dc, x, y)#FAILS IF PAST THE 1024x768 SIZE?	
		except:
			print "Coordinates ", x,",",y, "out of screen size"
			sys_exit(1)
		
		i_colour = int(long_colour)

	elif(x==-1):
		print "Missing 'y' coordinate"
		sys_exit(1)
	elif(y==-1):
		print "Missing 'x' coordinate"
		sys_exit(1)
	
	return (i_colour & 0xff), ((i_colour >> 8) & 0xff), ((i_colour >> 16) & 0xff)#magical bit-shifting

def get_hwnds_for_pid (pid):
	from win32gui import IsWindowEnabled, EnumWindows
	from win32process import GetWindowThreadProcessId 
	def callback (hwnd, hwnds):
		
		if (IsWindowEnabled (hwnd)):
			_, found_pid = GetWindowThreadProcessId(hwnd)
		
			if found_pid == pid:
				hwnds.append (hwnd)
			
		return True
	
	hwnds = []
	EnumWindows (callback, hwnds)
	
	return hwnds

def getProcessPID(target):
	"""
		Returns PID of given process name argument
	"""
	from psutil import get_pid_list, Process
	from string import lower
	from sys import exit as sys_exit
	
	EXCLUDED_PROCESSES=["audiodg.exe", "soffice.bin.exe", "system.exe", "svchost.exe", "system idle process.exe", "system", "system idle process"]
	
	resultPID=-9000
	target=lower(target)
	
	if ".exe" not in target:
		target=".".join([target,"exe"])
		
	
	
	if type(target)==str and target not in EXCLUDED_PROCESSES:
		
		for PID in get_pid_list():
			
			if lower(Process(PID).name) not in EXCLUDED_PROCESSES and lower(Process(PID).name)==target:
				resultPID=PID
				break
		
		if resultPID==-9000:
			print "No PID found for ", target
			print "Terminating script."
			sys_exit(1)
			
	
		
		
	else:
		print "Passed argument: ", target ," is invalid. Must be string type argument and not an exlucded process"
	
	
	return resultPID

def resizeWindow(width,height, processName="cmd",pid=-1):
	from win32gui import MoveWindow, GetWindowRect
	
	if pid==-1:
		processPID=getProcessPID(processName)	
	else:
		processPID= pid
		
	hwndList=get_hwnds_for_pid (processPID)	
	#hwnd=hwndList[0]
	for hwnd in hwndList:	
	
		
		winRect=GetWindowRect(hwnd)
		x=winRect[0]
		y=winRect[1]
		
	
	
		MoveWindow(hwnd,x,y,width,height,True)
	
def moveWindow(x, y, processName="", pid=-1, hwnd=-1, width=-1, height=-1):
	
	from win32gui import MoveWindow, GetWindowRect
	from sys import exit as sys_exit
	from pywintypes import error as pywintypesError
	"""
		Moves window of given process name/pid to the x,y coordinates given
		-Must be passed ONLY one argument: process name or a pid, but not both
	"""
	
	if type(processName)==int:
		processPID=processName
	
	elif len(processName)==0 and pid==-1:
		print "Must pass at least one argument, either process name or PID"
		sys_exit(1)
	
	elif len(processName)>0 and pid==-1:#case for just the process name passed
		
		if( processName.isdigit() ):#case for accidentally pid as first argument
			processPID=int(processName)

		else:
			processPID=getProcessPID(processName)
	
	elif len(processName)==0 and pid!=-1:
		processPID=pid
		
	else:
		print "Cannot have both process name and PID argument passed."
		
	
	hwndList=get_hwnds_for_pid (processPID)
	
	#if len(hwndList)==1:
	hwnd=hwndList[0]
	'''
	else:
		printNumberedList(hwndList)
		hwnd=chooseFromNumberedList(hwndList)
	'''
	
	'''
	else:
		print "Error. More than one instance of the process was found."
		print "List of PIDs found: ", hwndList
		sys_exit(1)
	'''
	if width==-1 and height==-1:
	
		try:
			rect=GetWindowRect(hwnd)#get window sizes to keep the window sizes similar when moving them
			width=rect[2]-rect[0]
			height=rect[3]-rect[1]
			
		except pywintypesError:
			print "Invalid window handle."
			sys_exit(1)
			
		
	
	MoveWindow(hwnd,x,y,width,height,True)

	
def getHandle(processName):
	try:
		return get_hwnds_for_pid( getProcessPID(processName) )[0]
	except IndexError:
		print "No handle found"
		return -1

def keyboardType(keyChar,targetProgram=""):
	from win32com import client
	from time import sleep
	
	"""
		Alt=%, CTRL=^, Shift=+
		Shift + F10= Context Menu/ Menu Key
		~ 	{~} 	send a tilde (~)
		! 	{!} 	send an exclamation point (!)
		^ 	{^} 	send a caret (^)
		+ 	{+} 	send a plus sign (+)
		Alt 	{ALT} 	send an Alt keystroke
		Backspace 	{BACKSPACE} 	send a Backspace keystroke
		Clear 	{CLEAR} 	Clear the field
		Delete 	{DELETE} 	send a Delete keystroke
		Down Arrow 	{DOWN} 	send a Down Arrow keystroke
		End 	{END} 	send an End keystroke
		Enter 	{ENTER} 	send an Enter keystroke
		Escape 	{ESCAPE} 	send an Esc keystroke
		F1 through F16 	{F1} through {F16} 	send the appropriate Function key
		Page Down 	{PGDN} 	send a Page Down keystroke
		Space 	{SPACE} 	send a Spacebar keystroke
		Tab 	{TAB} 	send a Tab keystroke
		
		{Ctrl+Esc} send Windows keystroke
	"""
	shell=client.Dispatch("WScript.Shell")
	if len(targetProgram)>0:
		shell.AppActivate(targetProgram)
	if(keyChar=="~"):
		shell.SendKeys( "{~}")
	elif(keyChar=="!"):
		shell.SendKeys( "{!}")
	elif(keyChar=="+"):
		shell.SendKeys( "{+}")
		
	elif(keyChar=="("):
		shell.SendKeys( "{(}")
	elif(keyChar==")"):
		shell.SendKeys( "{)}")
		
	else:
		shell.SendKeys(keyChar)

def getConsoleColor():
	from cmdColoring import getConsoleColor as gcc
	return gcc()

def setConsoleColor(color):#include string argument? color print, change color to original
	from cmdColoring import setConsoleColor as scc, COLOR_CHOICES
	
	if type(color)==int:
		scc(color)
	
	else:
		try:
			scc( COLOR_CHOICES[ "".join( ["FOREGROUND_", color.upper()] ) ] )
		except KeyError:
			errorMessage= "".join( ["Invalid foreground color: ", color ])
			errorAlert(errorMessage)
			
def printColored(text, color):
	origColor=getConsoleColor()
	setConsoleColor(color)
	print text
	setConsoleColor(origColor)
	
			
def errorAlert(msg=""):
	
	originalCmdFGColor=getConsoleColor()
	setConsoleColor("red")
	msg= "\nERROR: "+ msg
	print msg
	setConsoleColor(originalCmdFGColor)
	
	return msg
	

def takeScreenshot(appName=""):
	"""Takes screenshot of current window/ foreground"""
	
	from win32gui import GetDesktopWindow, GetWindowRect, GetWindowDC, ReleaseDC, GetWindowText, GetForegroundWindow
	from win32ui import CreateDCFromHandle, CreateBitmap
	from win32con import SRCCOPY
	from datetime import datetime
	from psutil import Process
	
	#appName=GetWindowText(GetForegroundWindow())
	if len(appName)==0:
		appName=Process( getPIDFromHandle(GetForegroundWindow()) ).name
	
	windowsHandle = GetDesktopWindow()

	rect=GetWindowRect(windowsHandle)
	width=rect[2]-rect[0]
	height=rect[3]-rect[1]
	left = rect[0] #win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
	top = rect[1] #win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)

	hwindc = GetWindowDC(windowsHandle)
	srcdc = CreateDCFromHandle(hwindc)
	memdc = srcdc.CreateCompatibleDC()
	dataBitMap = CreateBitmap()

	dataBitMap.CreateCompatibleBitmap(srcdc, width, height)
	memdc.SelectObject(dataBitMap)
	memdc.BitBlt((0, 0), (width, height), srcdc, (left, top), SRCCOPY)
	#fileName="".join(["SS_", appName,"_", str(datetime.now().strftime("%b-%d-%Y@%H_%M_%S")).strip(), ".png"])
	fileName="".join(["SS_", appName,"_", str(datetime.now().strftime("%b-%d-%Y@%H_%M_%S")).strip(), ".bmp"])
	print "Saved screenshot as :", fileName
	dataBitMap.SaveBitmapFile(memdc, fileName)

	srcdc.DeleteDC()
	memdc.DeleteDC()
	ReleaseDC(windowsHandle, hwindc) 
	
	return fileName
	
def getPIDFromHandle(handle):
	from psutil import get_pid_list, Process
	from string import lower
	EXCLUDED_PROCESSES=["audiodg.exe", "system.exe", "svchost.exe", "system idle process.exe", "system", "system idle process"]
	
	resultPID=-1
	
	for pid in get_pid_list():
		if lower(Process(pid).name) not in EXCLUDED_PROCESSES and handle in get_hwnds_for_pid( getProcessPID( Process(pid).name ) ):
			resultPID=pid
			break
	
	return resultPID
	
def cropImage(imageFileName, cropBox):
	import Image
	from random import randint
	
	img=Image.open(imageFileName)
	extension=imageFileName[imageFileName.rindex('.'):]
	frame=img.crop(cropBox)
	saveFileName="".join(["cropped_", imageFileName ,extension])
	frame.save(saveFileName)
	
	return saveFileName
	
	
def moveMouse(x,y):
	from mouseMacro import move
	if( type(x)==str and type(y)==str):
		try:
			x=int(x)
			y=int(y)
		except ValueError:
			print "Invalid arguments. Must be integer"
		
	if( type(x)==int and type(y)==int):
		move(x,y)
	else:
		print "Invalid arguments. Must be integer"
		
def getListFromPipeStr(pipePrintStr):
	
	pipedList= pipePrintStr.split('\n')
	for i in range(len(pipedList)-1,-1,-1):
		
		try:
			pipedList[i]=pipedList[i][pipedList[i].index("\"")+1: pipedList[i].rindex("\"")]
		except ValueError:
			pipedList.remove(pipedList[i])
			
	return pipedList
	
def drawLoadingBar(drawString):
	import sys
	drawString=str(drawString)
	sys.stdout.write(drawString)
	sys.stdout.write("\b"* len(drawString))
	sys.stdout.flush()
	
def __listGlobalVars():
	"""Lists the global variables in the current module"""
	from string import lower
	z=globals()
	for i in z.iterkeys():
		if("file" in lower(str(i)) or "log" in lower(str(i))):
			if(type(z[i])==str and "root" not in z[i]):
				print z[i]
				
				
def __backUpPyAndText():
	"""
		backs up .py and txt files
	"""
	
	from os import getcwd, listdir, getenv, path
	filesList=listdir(getenv("UtilResources"))
	pathStr=getenv("UtilResources")
	for i in range(len(filesList)-1,-1,-1):
		file=filesList[i]
		#if ".pyc" in file or ".exe" in file or ".java" in file or ".class" in file or ".c" in file or ".o" in file:
		extension=path.splitext(file)[1]#extension of file
		if (extension!=".py" and extension!=".txt" ):
			filesList.remove(file)
	
	
	
	from os import path
	for file in filesList:
		file="".join([pathStr,"\\",file])
		createBackUp(file)
	
	