r"""
Associates files with tags to facilitate and enable custom searches
"""

from os import getcwd, path
from sys import argv, stdin
from root import tagFile, getClipboardData, getInputFromKeyPress, createBackUp, standardizeString, switchBoard, printNumberedList, chooseFromNumberedList, setClipboardData
from TagObject import *
from string import lower
from threading import Thread
#REM "%1" in batch handles filenames with spaces
AVAILABLE_SWITCHES=['l','p','s']
def loadTagFile():
	"""
	Loads the contents of tagFile.txt into existingTagList to prevent repetitive opening of file when checking for the existance of multiple tags
	"""
	
	existingTagList=[]
	f=open(tagFile, "r")
	input=f.readline()
	
	while(input!=""):
		token=input.split()
		
		tag=Tag(getTag(token))
		fileNameList=getFileNameList(token)
		tag.setFileList(fileNameList)
		
		existingTagList.append(tag)
		
		input=f.readline()
	f.close()
	
	return existingTagList
		
def tagExists(tag, existingTagList):
	"""
	Checks if tag exists by comparing tag with each value in existingTagList until tag is found or length of existingTagList is reached
	"""
	result=False
	i=0
	
	while(result!=True and i<len(existingTagList)):
		
		if(lower(str(existingTagList[i].getTag()))==lower(str(tag))):
			result=True
		elif(lower(str(existingTagList[i].getTag()))>lower(str(tag))):
			i=len(existingTagList)
		i=i+1
	
	return result

def getTag(token):
	
	i=0
	tagName=""
	#REM: a tag can be more than one word, which is why we don't do tagName=token[0]
	while(i<len(token)):
		if "c:" not in standardizeString(token[i]):
			tagName="".join([tagName," ",token[i]])
		else:
			i=len(token)
		i=i+1
	
	tagName=tagName.strip()
	
	return tagName

def getFileNameList(token):
	"""
	Concatenates the file path to the name of the file from token[1] to token[len(token)-1]
	token[0] is the name of the tag
	"""
	
	start=False
	fullFileName=""
	fileNameList=[]
	i=1#tag must be atleast 1 string, so token[0] can be tag
	
	while(i<len(token)):
		
		if( ("\"") in token[i][0]):
			start=True
		
		if(start==True):
			fullFileName="".join([fullFileName,token[i]," "])
		
		if( ("\"") in token[i][len(token[i])-1] ):
			fileNameList.append(fullFileName.strip())
			fullFileName=""
		i=i+1
	
		fileNameList=sorted(fileNameList, key= str.lower)
	
	return fileNameList
	

def writeToFile(tagList, mode):
	"""
	Writes tags and their corresponding files to tagFile.txt
	Mode can either be [a]ppend or [w]rite
	Append is used when adding new tags
	Write is used when sorting and overwriting the whole text file
	"""
	
	if( (len(tagList)>0 and isinstance(tagList[0],Tag)) and (mode=="a" or mode=="w")):
		createBackUp(tagFile)
		#Thread(target=createBackUp, args=(tagFile,)).start()
		
		f=open(tagFile, mode)
	
		for i in range(0,len(tagList)):
			
			fileList=tagList[i].getStringList()
			if(len(fileList)>0):
				s="".join([tagList[i].getTag().strip()," ",fileList])#choosing not to standardizeString because some tags require to be capitalized such as DIY
				
				f.write(s)
				f.write("\n")
			#s="".join([str(tagList[i][0]),str(tagList[i][1])])
			#print s		
				
		f.close()
	
	else:
		print "Invalid mode"
	
def addNewTag(tagList,mode):
	
	writeToFile(tagList,mode)
	
def appendFile(existingTagList, tag, fileName):
	"""
	Reads tagFile.txt
	Appends fileName to the corresponding existing tag
	Overwrites tagFile.txt with new fileName attached to proper tag
	"""

	i=0
	while(i < len(existingTagList)):
		
		if(standardizeString(existingTagList[i].getTag())==standardizeString(tag.strip())):
			
			
			if(standardizeString(fileName) not in existingTagList[i].getStringList()):
				existingTagList[i].addToFileList(fileName)
				
			else:
				print "File already has",existingTagList[i].getTag(), "tag "
				
			i=len(existingTagList)
		i=i+1
	
	
	#Not relevant, only kept for reference: [0:-1] is substring slice to remove ':' char
		
	#existingTagList=sorted(existingTagList, key=lambda tag: lower(tag.getTag()))
	
	#writeToFile(existingTagList,"w")
	
def addTag(fileName, input=""):#input kwargs for use with piping (vlc.t)
	"""
	Prompts user to enter tag(s) to associate with file
	If tag doesn't assist, calls addNewTag(tagList, mode)
	Else calls appendFile(tagList, mode)
	tagList is the list of tag(s) in sorted order
	"""
	
	if(len(input)==0):
		input=raw_input("Enter tag(s). Separate using commas.\n")
	
	token=input.split(",")
	
	existingTagList=loadTagFile()
	
	appended=False
	for i in range(0,len(token)):
		tag= Tag((token[i]).strip())
		
		if(tagExists(tag.getTag(),existingTagList)==False):
			print "Creating new tag: ", tag.getTag()
			tag.addToFileList(fileName)
			existingTagList.append(tag)
		
		else:
			appendFile(existingTagList, tag.getTag(), fileName)
			appended=True
			
	
	if(appended==False):
		existingTagList=sorted(existingTagList, key=lambda tag: lower(tag.getTag()))
		addNewTag(existingTagList,"w")#==writeToFile but too stubborn to change name
		
	else:
		#these used to be in the appendFile method, moved here for efficiency, stops multiple writes, and only writes once when all the files have been appended
		existingTagList=sorted(existingTagList, key=lambda tag: lower(tag.getTag()))
		
		writeToFile(existingTagList,"w")

#passed a list of files to be tagged with given tag
def tagMultipleFiles(list,tag):
	existingTagList=loadTagFile()
	tagNotFound=True	
	
	for i in range(0,len(existingTagList)):
		
		if(lower(str(existingTagList[i].getTag()))==lower(str(tag.strip()))):
			tagNotFound=False

			for j in range(0,len(list)):
				
				if( str(list[j]).strip() not in existingTagList[i].getStringList()):	

					if( "C:" in str(list[j]).strip() ):
						
						if("\"" not in str(list[j].strip())):
							existingTagList[i].addToFileList("".join(["\"",list[j],"\""]))

						else:
							existingTagList[i].addToFileList(list[j])
							
						

					else:
						print "Invalid fileName, missing C: drive path"
				
			break

		elif(lower(str(existingTagList[i].getTag()))>lower(str(tag))):
			break


	if(tagNotFound==True):
		
		newTag=Tag(tag)
		print "Creating new tag: ", newTag.getTag()
		for i in range(0,len(list)):
			if("\"" not in str(list[i].strip())):
				newTag.addToFileList("".join(["\"",list[i],"\""]))
			else:
				newTag.addToFileList(list[i])
				
		existingTagList.append(newTag)
		existingTagList=sorted(existingTagList, key=lambda tag: lower(tag.getTag()))

		
	
	writeToFile(existingTagList,"w")

if __name__ == "__main__":
	
	switches=switchBoard(argv,  AVAILABLE_SWITCHES)	
	
	if(stdin.isatty()==False): #for vlc.t pipe tagging
		
		if 'l' in switches: # tag list :o
			pipedList=stdin.read().split('\n')
			
			for i in range(len(pipedList)-1,-1,-1): #omitted last one on purpose because it is assumed that this is used with nf -p, and the last item == first item
				try:
					pipedList[i]=pipedList[i][ pipedList[i].index("\"")+1 : pipedList[i].rindex("\"") ]
					
					
					if (path.isabs(pipedList[i]) ==False):
						pipedList[i]= "".join(["\"",getcwd(),"\\",pipedList[i],"\""])
					
				except:
					pipedList.remove( pipedList[i] )
			
			promptStr="Enter tag(s) for the following list. Separate using commas."
			
			pipedList=pipedList[:-1]
			printNumberedList(pipedList)
			
			tags=getInputFromKeyPress(promptStr)#using this because raw_input can't be used whilst piping
			print tags
			
			tagMultipleFiles(pipedList, tags)
		else:
				
			stdin.readlines()#prevents deconstructor error 
			print "Accessing pipes"
			fileName=getClipboardData()
			print fileName
			promptStr="Enter tag(s). Separate using commas."
			tags=getInputFromKeyPress(promptStr)#using this because raw_input can't be used whilst piping
			print tags
			
			addTag(fileName, tags)
	
	elif('p' in switches):
		
		existingTagList=loadTagFile()
		
		tL= []
		for tagObject in existingTagList:
			tL.append( tagObject.getTag())
		
		printNumberedList(tL)
		
		if('s' in switches):
			choice=chooseFromNumberedList(tL)
			setClipboardData(tL[choice])
	elif(len(argv)>1):
		
		if(("\\" in argv[1])==False):
			fileName="".join(["\"",getcwd(),"\\",argv[1],"\""])
		else:
			fileName="".join(["\"",argv[1],"\""])
		
		addTag(fileName)
	
	
	
	else:
		print "Missing parameter(s)"
		
	


