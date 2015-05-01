"""

-stores the newest file in the current working directory into clipboard

USAGE: nF [-d dir][strings in file...][-p][-s][-a]
-p: print list containing the given strings
-s: select from given list
-a: list is printed alphabetically instead of by creation data
"""
#-f for files only, ignore dir in newest file result

from sys import argv, float_info, stdin
from string import lower
from directPicToFolder import getFolder
from root import picDir, switchParser, addMember, setClipboardData, printNumberedList, chooseFromNumberedList, cen, inSwitchList, pipedList as pipedF, printList, chooseFromList, errorAlert, pipedList
from threading import Thread
from os import listdir, getcwd, stat, path
from sys import exit as sys_exit
AVAILABLE_SWITCHES=['p','s','d','h','a','#']
 	
def sortByCreationTime(fList):
	for i in range(len(fList)-1,-1,-1):
		try:
			fList[i]=addMember(fList[i],stat)	
		except WindowsError:
				fList.remove(fList[i])
				print "Removing", fList[i].encode('ascii','ignore')
		
		
	fList=sorted(fList, key=lambda Metamorph:Metamorph.getAttribute().st_ctime, reverse=True)
	
	fList=map(str, fList)
	
	return fList
		
def getNewestFileList(targDir=getcwd()):
	fList= listdir(targDir)
	fList=sortByCreationTime(fList)
	return fList

def pruneFileList(fList, targWords):
	for f in fList[:]:
		for word in targWords:
			if word not in f:
				fList.remove(f)
				break
				
	return fList

def presentResult(fList, targDir=getcwd()):
	
	if 'p' in switches:
		numItemsToPrint= 10
		
		if '#' in switches:
			numOfItemsToPrint=int(switches['#'])
		
		if len(fList)<numItemsToPrint:
			numItemsToPrint=len(fList)
		
		aes="full"
	
				
			
	elif len(switches)==0:
		numItemsToPrint= 1
		aes="none"
		
	if numItemsToPrint>1:
		printList(fList, numItemsToPrint, aes)
	
	if 's' in switches:
			
		if len(switches['s'])>0:
			sVal=int( switches['s'] )
			if sVal <=len(fList):
				choice=fList[ sVal-1]
			else:
				errorAlert("Select switch value:" + str(sVal) + " greater than list size: " + str(len(fList)) )
				exit(1)
		else:
			choice=chooseFromList(fList)
		
		fList[0]=choice
	
	fList[0]="\""+ targDir+"\\"+str(fList[0]) + "\""
	print fList[0]
	
	setClipboardData(fList[0])
	
	
		

if __name__ == "__main__":	
	switches=switchParser(argv,  AVAILABLE_SWITCHES)	
	
	
	if('h' in switches):
		print __doc__
		
	elif( stdin.isatty()==False):
		
		print "Piping"
		
		fList=pipedList("".join(map(str,stdin.readlines())))
		prunedList=pruneFileList(fList, argv[1:])
		sortByCreationTime(prunedList)
		presentResult(fList)
		
	else:
		fList=getNewestFileList()
		prunedList=pruneFileList(fList, argv[1:])
		presentResult(prunedList)
