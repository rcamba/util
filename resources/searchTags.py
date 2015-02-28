"""
*Not using .bat because it reads commas as a separator/delimiter
"""
from sys import argv
from root import switchParser, printList, setClipboardData, chooseFromList
from tag import getFilenameList
from string import strip
AVAILABLE_SWITCHES=['s']


if __name__=="__main__":
	switches=switchParser(argv)
	
	
	tagList= " ".join(map(str, argv[1:])).split(',')
	tagList=map(strip,tagList)
	
	
	fileList = getFilenameList( tagList)
	
	for i in range(0,len(fileList)):
		fileList[i]="\""+fileList[i]+"\""
	
	
	printList( fileList )
	
	
		
	
	if "s" in switches:
		if len(fileList)==1:
			choice=fileList[0]
		else:
			choice=chooseFromList(fileList)
		
		#setClipboardData( "\""+ choice+"\"")
		setClipboardData(choice)
		
		