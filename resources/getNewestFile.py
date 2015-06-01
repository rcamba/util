"""
stores the newest file in the current working directory into clipboard

USAGE: nF [target string] [[-p][-#]] [-s][-f][-d]
-p: print list containing the given strings
-#:[num] number of items to print
-s: select from given list
-f: list FILES only
-d: list DIRECTORIES
"""


from sys import argv, stdin, stdout
from root import switchParser, addMember, setClipboardData, cen, printList, chooseFromList, errorAlert, pipedList
from threading import Thread
from os import listdir, getcwd, stat, path
from sys import exit as sys_exit
from string import lower
AVAILABLE_SWITCHES=['p','s','d','h','f','#']

def sortByCreationTime(fList):
	for i in range(len(fList)-1,-1,-1):
		try:
			fList[i]=addMember(fList[i],stat)
		except WindowsError:
				fList.remove(fList[i])
				print "Removing", fList[i].encode('ascii','ignore')


	fList=sorted(fList, key=lambda Metamorph:Metamorph.getAttribute().st_ctime, reverse=True)

	fList=map(str, fList)
	for i in range(0,len(fList)):
		fList[i]="\""+fList[i]+"\""

	return fList

def getFileList(targDir=getcwd()):
	fList= listdir(targDir)
	fList= map(lower, fList)
	return fList

def pruneFileList(fList, targWords):

	for f in fList[:]:
		removed=False

		for word in targWords:
			if word not in f:
				fList.remove(f)
				removed=True
				break

		if removed==False:
			if 'f' in switches:
				if path.isfile(f)==False:
					fList.remove(f)

			elif 'd' in switches:
				if path.isdir(f)==False:
					fList.remove(f)

	return fList


def printSettings():
	numItemsToPrint= 1
	aes="none"

	if 'p' in switches:
		numItemsToPrint= 10

		if '#' in switches:
			numItemsToPrint=int(switches['#'])

		if len(fList)<numItemsToPrint:
			numItemsToPrint=len(fList)

		aes="full"

	return (numItemsToPrint, aes)

def handleSelect(fList):
	if 's' in switches:

		if len(switches['s'])>0:
			sVal=int( switches['s'] )
			if sVal <=len(fList):
				choice=fList[ sVal-1]
			else:
				errorAlert("Select switch value:" + str(sVal) + " greater than list size: " + str(len(fList)) )
				sys_exit(1)
		else:
			choice=chooseFromList(fList)

		fList[0]=choice

	return fList[0]

def presentResult(fList, targDir=getcwd()):
	#default values when empty switches

	numItemsToPrint, aes= printSettings()

	if numItemsToPrint>1:
		printList(fList, numItemsToPrint, aes, pressToContinue=stdout.isatty())

	fList[0]=handleSelect(fList)


	if path.isabs(fList[0].replace("\"",''))==False:
		fList[0]="\""+ targDir+"\\"+str(fList[0]).replace("\"",'') + "\""
		#fList[0]=path.abspath(fList[0])

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
		finalList=sortByCreationTime(prunedList)

	else:

		fList=getFileList()
		prunedList=pruneFileList(fList, argv[1:])
		finalList=sortByCreationTime(prunedList)


	if len(prunedList)>0:
		presentResult(finalList)
	else:
		errorAlert("Empty list")
