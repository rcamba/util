"""
*Not using .bat because it reads commas as a separator/delimiter
"""
from sys import argv, stdin, stdout
from root import switchParser, printList, setClipboardData, chooseFromList, pipedList
from tag import getFilenameList, getTagList
from string import strip
AVAILABLE_SWITCHES=['s','f']

def main(argList):
	if 'f' in switches:
			
		tagList=getTagList(argList[0])
		print tagList

	else:
		tagList= " ".join(map(str, argList)).split(',')
		tagList=map(strip,tagList)
		fileList = getFilenameList( tagList)
		
		for i in range(0,len(fileList)):
			fileList[i]="\""+fileList[i]+"\""
		
		if 's' in switches:
			if len(switches['s'])>0:
				choice=fileList[int (switches['s'])-1]
			
			else:
				printList( fileList, pressToContinue=stdout.isatty() )
			
				if len(fileList)==1:
					choice=fileList[0]
				
				else:
					choice=chooseFromList(fileList)
				
			print choice
			setClipboardData(choice)
		
		else:
			printList( fileList, pressToContinue=stdout.isatty() )
		
if __name__=="__main__":
	switches=switchParser(argv)
	
	
	if stdin.isatty()==False:#for using with nf/search
		print "Piped search"
		argList=pipedList( "".join(map(str,stdin.readlines())) )
		main(argList)
	
	elif len(argv)>1:	
		main(argv[1:])
		
			
	else:
		
		tList=getTagList()
		tList.sort()
		printList(tList)
		choice=chooseFromList( tList )
		cfList=  getFilenameList(choice)
		printList(cfList)
		choice=chooseFromList( cfList)
		setClipboardData ( choice)