from root import dirJumpFile, printList, chooseFromList, prevDirFile, switchParser, createBackUp, errorAlert
from sys import argv
from string import lower, strip
from os import getcwd


AVAILABLE_SWITCHES=['a','d']

def writeToPrevDirFile(prevDir):
	f=open(prevDirFile,"w+")
	f.write(prevDir)
	f.close()

def sortDirJump(targPosition):
	
	jumpList=getJumpList()
	jumpList[0]= jumpList[targPosition]
	writeToPrevDirFile(getcwd())
	writeDirJump(jumpList)
	
def addToDirJump(targDir):
	createBackUp(dirJumpFile)
	print "Adding: " + targDir
	f=open(dirJumpFile,"a")
	f.write(str( getcwd() ) )
	f.close()	
	
def removeFromDirJump(targPosition):
	jumpList=getJumpList()
	print "Removing: " + jumpList[targPosition]
	jumpList.remove(jumpList[targPosition])
	writeDirJump(jumpList)
	
def writeDirJump(fList):
	#createBackUp(dirJumpFile) - don't want to back it up every single jump
	f=open(dirJumpFile,"w")
	for file in fList:
		f.write(file)
		f.write("\n")
	f.close()
	
def getJumpList():
	f=open(dirJumpFile,"r")
	lineList=f.readlines()
	f.close()
	
	lineList=map(strip,lineList)
	
	return lineList
	
if __name__ == "__main__":
	switches=switchParser(argv)
	if 'a' in switches:
		addToDirJump(getcwd())
		
	elif 'd' in switches:
		try:
			targPosition=int(switches['d'])
		except ValueError:
			errorAlert("-d must contain int selecting directory to be removed from jump list")
		removeFromDirJump(targPosition)
	
	elif len(argv)>1:
		try:
			targPosition=int(argv[1])
		except ValueError:
			errorAlert("# out of directory listing")
		sortDirJump(targPosition)
	
	else:
		jumpList= getJumpList()
		printList( jumpList[1:] )
		choice=chooseFromList( jumpList[1:])
		sortDirJump(jumpList.index(choice))#+1 for skipping first line of jumped route