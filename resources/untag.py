from tag import loadTagFile, writeToFile
from sys import argv, exit as sys_exit
from os import getcwd, path
from root import printNumberedList, standardizeFile, standardizeString, switchBoard
AVAILABLE_SWITCHES=['f','t']
def listAssociatedFiles(token):
	
	tagName=""
	
	
	for i in range(0,len(token)):
		tagName="".join([tagName," ",token[i]])
	tagName=tagName.strip()
	
	
	print "Searching for tag: ", tagName
	
	fileList=""
	
	for i in range(0,len(existingTagList)):
		if standardizeString(existingTagList[i].getTag())==standardizeString(tagName) :
			fileList=existingTagList[i].getFileList()
			tagPosition=i
	
	if(len(fileList)==0):
		print "Tag not found"
	else:
		
		print "Files associated with: ", tagName
		printNumberedList(fileList)
		
		input=raw_input("\nEnter the number(s) of the file(s) you want to delete separated by spaces\n")
		token=input.split()#token passed overwriten
		
		token.sort()
		for i in range(len(token)-1,-1,-1):
			if(len(fileList)>int(token[i])-1 and int(token[i])>0):
				existingTagList[tagPosition].removeFromFileList(fileList[int(token[i])-1])
			else:
				print "Number out of bounds"
				
		writeToFile(existingTagList,"w")

def listAssociatedTags(fileName):
	global tagList
	global positionList
	existingTagList=loadTagFile()
	if (__name__ == "__main__")==False:
		tagList=[]
		positionList=[]
	
	if(len(fileName)==0):
		print "Missing filename"
		sys_exit()###<------------------
	
		
	elif path.isdir(path.split(fileName)[0])==False:
		fileName="".join([getcwd(),"\\",fileName])
		
	
	fileName="".join(["\"",fileName,"\""])
	
	
	for i in range(0,len(existingTagList)):
		
		if( standardizeFile(fileName) in standardizeFile(existingTagList[i].getStringList()) ):
			tagList.append(existingTagList[i].getTag())
			positionList.append(i)
	
	return tagList
	
		
def examineTagList( tagList, fileName):
	if(len(tagList)==0):
		print "No tag(s) found for: ", fileName
	else:
		
		print "Tags associated with: ", fileName
		printNumberedList(tagList)
		if __name__ == "__main__":#for searchTags using it to simply print tags associted w/ a given file
			input=raw_input("\nEnter the number(s) of the file(s) you want to delete separated by spaces\n")
			token=input.split()#token passed overwritten
			token.sort()
			for i in range(len(token)-1,-1,-1):		
				
				if(len(tagList)>int(token[i])-1 and int(token[i])>0):
					position=tagList.index(tagList[int(token[i])-1])
					
					existingTagList[int(positionList[position])].removeFromFileList(fileName)
				
				else:
					print "Number out of bounds"
				#print existingTagList[int(positionList[position])].getTag(), existingTagList[int(positionList[position])].printFileList()
			
			writeToFile(existingTagList,"w")
	
	
		
if __name__ == "__main__":
	switches=switchBoard(argv, AVAILABLE_SWITCHES)
	
	
	if(('t') in switches):
		existingTagList=loadTagFile()
		listAssociatedFiles(argv[1])
	elif(('f') in switches):
		fileName=argv[1]
		
		if( path.isabs(fileName)==False):
			print "Argument must be full file path because you are lazy"
			exit(1)
		
		fileName="\""+argv[1]+"\""
		existingTagList=loadTagFile()
		positionList=[]
		tagList=[]
		tagList=listAssociatedTags(argv[1])
		
		
		print "Searching for file: ", fileName
		examineTagList( tagList, fileName)
	else:
		print "Invalid parameters"
		print "Usage untag[-f filename][-t tag]"
	
	