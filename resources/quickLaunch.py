from root import quickLaunchFile, printNumberedList, chooseFromNumberedList, prevDirFile
from sys import argv
from string import lower
from os import getcwd
def createQL():	
	f=open(quickLaunchFile,"r")
	f.readline()
	f.readline()
	dirList=f.readlines()
	
	for i in range(0,len(dirList)):
		if(len(dirList[i])>0):
			dirList[i]=dirList[i].replace("\n","")
		else:
			dirList.remove(dirList[i])
	f.close()
	
	return dirList

def writeQL(list, target=-1):
	
	if(target==-1):
		print "Quick Launch:"
		printNumberedList(list)
		choice=chooseFromNumberedList(list)
		if(str(choice).isdigit()):
			target=int(choice)
		else:
			print "Invalid choice"
		
		target=target+1#I DONT KNOW WHY BUT THIS WORKS; I THINK IT COUNTERS THE -1 FROM CHOICE
		
	if( (target-1)<len(list) ):
		
		
		
		#re-Write
		f=open(quickLaunchFile,"w")
		f.write(list[target-1])
		f.write("\n\n")
		for i in range(0,len(list)):
			f.write(list[i])
			f.write("\n")
		f.close()
		
	else:
		print "Number out of range"
	

def writeToPrev( dirName):
	f=open(prevDirFile,"w")
	f.write(  dirName)
	f.write("\n")
	f.close()
	
if __name__ == "__main__":
	writeToPrev(getcwd())
	QL=createQL()
	if(len(argv)<2):
		writeQL(QL)
	
		
	else:	
		QL=createQL()
		
		if(argv[1].isdigit()):
			writeQL(QL, int(argv[1]))
		else:
			print "Invalid argument"