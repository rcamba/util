"""

-stores the newest file in the current working directory into environment variable "nF"
-can be accessed by "%nF%": 
--REPLACED: value is now stored into clipboard

USAGE: nF [-d dir][strings in file...][-p][-s][-a]
-p: print list containing the given strings
-s: select from given list
-a: list is printed alphabetically instead of by creation data
"""


from sys import argv, float_info, stdin
from string import lower
from directPicToFolder import getFolder
from root import picDir, switchBoard, addMember, setClipboardData, printNumberedList, chooseFromNumberedList, cen, inSwitchList, pipedList as pipedF
from threading import Thread
from os import listdir, getcwd, stat, path
from sys import exit as sys_exit
AVAILABLE_SWITCHES=['p','s','d','h','a','#']
 
def getDir():
	
	if("d" in switches):#args: fileName, /d, dir
		
		if(len(argv[1])==1):
			folder=getFolder(str(argv[1]))#gets folder associated with letter from spic
		elif( ("http" in str(argv[1]) )==True ):
			folder=picDir#folder is main pic folder
		else:
			folder=str(str(argv[1]))
	
	else:
		folder=getcwd()
	
	return folder
	
def getStringList():
	
	stringList=[]
	for i in range(1,len(argv)):
		if(str(argv[i]).strip() not in switches):
			stringList.append(str(argv[i]).strip())
	
	return stringList
	
def getString():
	
	string=""
	for i in range(1,len(argv)):
		string="".join([string," ",str(argv[i])])
		
	string=string.strip()
	
	return string
	
def getNewestFromList(list, fromPipe=False):
	
	max=float_info.min
	maxFile=""
	
	
	for i in range(0,len(list)):
		if(fromPipe==False):
			file="".join([dir,"\\",list[i]])
		else:
			file=list[i]
		
		
		if(path.exists(file)):
			var_stat= stat( file )
			
			if(var_stat.st_ctime> max):			
				maxFile=list[i]
				max=var_stat.st_ctime
		
	return  maxFile

def getNumOfItemsToPrint(max):
	
	numOfItemsToPrint=10
	
	switchesString=" ".join(map(str,switches))
	if('#' in switchesString):
		#look for 'n' switch
		for i in switches:
			
			if i[0]=='#':
				
				numOfItemsToPrint=i[1]
				
				#print numOfItemsToPrint
				
				if(numOfItemsToPrint.isdigit()):
					numOfItemsToPrint=int(numOfItemsToPrint)
					
				else:
					print "Invalid number with n switch"
					sys_exit()
	
	if(int(numOfItemsToPrint)>max):
		numOfItemsToPrint=int(max)
	
	return numOfItemsToPrint
	
def getNewest(stringList,directory):
	
	"""
	Enters all files in current directory into a list
	Takes the stat of each file and compares their creation date as floats
	File with the largest (float) value is the newestFile
	set nF to clipBoard
	-default action for paramter is to use it to return the newestFile that contains that string
	-d will be the optional switch to specify that parameter is a directory
	"""
	
	
	locList=listdir(directory)
	
	
	if(len(stringList)>0):
		
		for i in range(0,len(stringList)):
			j=len(locList)-1
			while(j>-1):		
				if(lower(stringList[i]) not in lower(locList[j])):
					locList.pop(j)
				
				j=j-1
		
	maxFile=getNewestFromList(locList)
	eleNum=0
	#print maxFile, "\n"
	if(len(maxFile)>0):
		nF=maxFile.strip()
		path=directory#os.path.dirname(__file__)
		nF="".join(["\"",path,"\\",nF,"\""])
	
		if("p" in switches): 
			
			
			numOfItemsToPrint=getNumOfItemsToPrint(len(locList))
				
			if(len(stringList)>0):
				switchesString=" ".join(map(str,switches))
				if ('#' in switchesString):
					orderedByCTimeList=printSwitch(locList,numOfItemsToPrint)
				else:
					orderedByCTimeList=printSwitch(locList)
					numOfItemsToPrint=len(locList)
			else:
			
				orderedByCTimeList=printSwitch(locList,numOfItemsToPrint)
			
			locList=locList[:numOfItemsToPrint]
			
			
			
			
			if("s" in switches):
				eleNum=chooseFromNumberedList(locList, True )
				nF="".join(["\"",path,"\\",str(orderedByCTimeList[eleNum]),"\""])
				
			else:
				for i in range(0,len(switches)):
					if type(switches[i])==tuple:
						if 's' in switches[i]:
							nF="".join(["\"",path,"\\",str( orderedByCTimeList [ int(switches[i][1])-1 ] ),"\""]) 
				
	
	else:
		nF="Search strings not found"
	
	if(eleNum!=-1):
		cen()
		
		#setClipboardData(nF)
		Thread(target=setClipboardData, args=(nF,)).start()
		#print nF
	
	
def printSwitch(printList,endRange=-1):
	from copy import copy
	
	#print "Print switch on:"
	
	if('a' in switches):
		rPrintList=sorted(printList, key=str.lower)
	
	else:
		for i in range(len(printList)-1,-1,-1):
			try:
				printList[i]=addMember(printList[i],stat)
			except WindowsError:
				printList.remove(printList[i])
		
		try:
			printList=sorted(printList, key=lambda Metamorph:Metamorph.getAttribute().st_ctime, reverse=True)
		except:
			print "Failed to sort list"
		
		
		rPrintList=copy(printList)
		for i in range(0,len(printList)):
			fNameHolder=printList[i].getObject()
			
			rPrintList[i]=fNameHolder
			printList[i]="".join(["\"",fNameHolder,"\""])
		
		
		
	if(endRange==-1):
		printNumberedList(printList)
	else:
		printNumberedList(printList,endRange)
	

	

	return rPrintList
	
def getNewestFromPipe(stringList, pipedList):
	"""pipedList gets cleaned to be just filepaths, then proceed regularly"""
	def cleanList(pipedList):
		
		for i in range(len(pipedList)-1,-1,-1):
			
			try:
				pipedList[i]=pipedList[i][pipedList[i].index("\"")+1: pipedList[i].rindex("\"")]
			except ValueError:
				pipedList.remove(pipedList[i])
	
	
	
	
	#cleanList(pipedList)
	
	
	pipedList=pipedF(pipedList)
	
	
	if(len(stringList)>0):
		
		for i in range(0,len(stringList)):
			j=len(pipedList)-1
			while(j>-1):		
				if(lower(stringList[i]) not in lower(pipedList[j])):
					pipedList.pop(j)
				j=j-1
	
	if(len(pipedList)==0):#***
		print "Empty pipes. Terminating."
		sys_exit()
	
	maxFile=getNewestFromList(pipedList, fromPipe=True)
	
	eleNum=0
	
	if(len(maxFile)>0):
		nF="".join(["\"",maxFile.strip(),"\""])
		
		if("p" in switches): 
		
			if(len(stringList)>0):
				orderedByCTimeList=printSwitch(pipedList)
			else:
				numOfItemsToPrint=10
				
				switchesString=" ".join(map(str,switches))
				
				if('#' in switchesString):
					#look for 'n' switch
					for i in switches:
						if i[0]=='#':
							numOfItemsToPrint=i[1]
							
							if(numOfItemsToPrint.isdigit()):
								numOfItemsToPrint=int(numOfItemsToPrint)
								
							else:
								print "Invalid number with n switch"
								sys_exit()
				
				if(int(numOfItemsToPrint)>len(pipedList)):
					numOfItemsToPrint=int(len(pipedList))
								
				orderedByCTimeList=printSwitch(pipedList,numOfItemsToPrint)
				pipedList=pipedList[:numOfItemsToPrint]
			
			
			
			if( inSwitchList("s",switches) ):
				eleNum=chooseFromNumberedList(pipedList )
				
				nF="".join(["\"",str(orderedByCTimeList[eleNum]),"\""])
				
			elif len( [string for string in switches if "s" in string and type(string)==tuple]) > 0 :
				
				choice=int([string for string in switches if "s" in string and type(string)==tuple][0][1])-1
				nF="".join(["\"",str(orderedByCTimeList[choice]),"\""])
			
			
				
				
	
	else:
		nF="Search strings not found"
	
	if(eleNum!=-1):
		cen()
		setClipboardData(nF)
		#print nF
	
	
	
	


if __name__ == "__main__":	
	switches=switchBoard(argv,  AVAILABLE_SWITCHES)	
	
	
	if('h' in switches):
		print __doc__
		
	elif( stdin.isatty()==False):
		
		print "Piping"
		#stdinList=stdin.read().split('\n')#neccessary, I guess cause at the end of the method it invokes file object desctructor; prevents "close failed in file object destructor: sys.excepthook is missing; lost sys.stderr"
		
		stringList=getStringList()
		getNewestFromPipe(stringList,"".join(map(str,stdin.readlines())))
				
		
	
	elif( ("d") in switches ):#for handling spic.bat
		dir=getDir()
		getNewest("",dir)
	
	else:
		dir=getDir()
		stringList=getStringList()
		getNewest(stringList,dir)
	
