from os import path, getcwd
from root import errorAlert, removedFilesLog, chooseFromList, printList, createBackUp, setClipboardData
from string import rstrip, lower
from re import findall
from collections import OrderedDict
from sys import argv
import inspect

def logRemovedFile(msg):
	writer=open(removedFilesLog,'a')
	writer.write(msg)
	writer.close()


def validateFilenameList(filenameList, assocTag=""):
	
	
	if type(filenameList)==str:
		file=filenameList
		
		filenameList=[]
		filenameList.append(file)
		
	validFileList=[]
	
	for file in filenameList:
		
		if path.isabs(file)==False:
			file=getcwd()+'\\'+file
		
		
		if path.isfile(file)==False:
			if inspect.stack()[1][3]=="addTag":# methodName
				msg=errorAlert("Unable to add to tag" + assocTag + ". "+ file + " is an invalid file. ")
			elif inspect.stack()[1][3]=="loadTagDict":
				msg=errorAlert(file + " is an invalid file. Removed from "+ assocTag +" tag.")
			logRemovedFile(msg)
			
		else:
			validFileList.append(file)
			

		
	return validFileList


	
def addTag(tag, filenameList):
	
	validFileList=validateFilenameList(filenameList, tag)
	
	tagDict=loadTagDict()
	
	if tagDict.has_key(tag):
		tagDict[tag].extend(validFileList)
		if len(tagDict[tag])!=set(tagDict[tag]):#check for duplicates i.e tag already has file in its filelist
			duplicateList= list (set([x for x in tagDict[tag] if tagDict[tag].count(x) > 1]) )
			
			for d in duplicateList:
				print d, "already has tag:", tag
		
		#tagDict[tag]= list(set(tagDict[tag])) #remove files in same tag
	else:
		tagDict[tag]=validFileList
		print "Creating new tag: ", tag
	
	__writeTagFile__(tagDict,validFileList)
	
def __writeTagFile__(tagDict,validFileList):
	
	createBackUp(tagFile)
	writer=open(tagFile,'w') 
	
	tagDict=OrderedDict(sorted(tagDict.items(), key=lambda t: lower(t[0])))
	
	for key in tagDict.keys():
		
		fileList=tagDict[key]
		
		if len(fileList)>0:
			writer.write(key+"::")
			for file in fileList:

				writer.write("\"" + lower(file) + "\" ")
				
			writer.write("\n")
	
	writer.close()
		
	
	
def convertToFilenameList(fileStringList):
	res=[]
	
	fileStringList=findall('".+?"', fileStringList)
	
	for fileStr in fileStringList:
		res.append( fileStr.replace('\"','') )
	
	return res
	
def loadTagDict():
	
	reader=open(tagFile)
	lineList=map(rstrip, reader.readlines())
	
	tagDict={}
	changes=False
	for line in lineList:
		
		tag, fileStringList=line.split('::')
		tag=lower(tag)
		
		filenameList=convertToFilenameList(fileStringList)
		validFileList=validateFilenameList(filenameList, tag)
		tagDict[tag]=validFileList
		
		if len(filenameList)!=len(validFileList): #changes to filelist: a file was removed
			changes=True
			
	if changes==True:
		__writeTagFile__(tagDict, validFileList)
		
	return tagDict
	
def getFilenameList(tagList):#str or list
	if type(tagList)==str:
		tagList=[tagList]
	
	tagDict=loadTagDict()
	
	result=[]
	
	counter=0
	for tag in tagList:
		tag=lower(tag)
		if tagDict.has_key(tag):
			if counter>0:
				result=list(set(tagDict[tag]).intersection(set(result)))
			else:
				result.extend(tagDict[tag])
		else:
			errorAlert("Tag doesn't exist:" + tag)
		counter=counter+1
		
	return result
	

	
def getTagList(filename):
	tagDict=loadTagDict()
	
	tagList=[]
	for key in tagDict.keys():
		if filename in tagDict[key]:
			tagList.append(key)
			
	return tagList
	

	
if __name__=="__main__":
	tagFile=r"C:\Users\Kevin\Util\resources\tagFile.txt"
	
	if len(argv)>1:
		tagList=raw_input("Enter tag(s). Separate with commas\n").split(',')
		
		
		for tag in tagList:
			addTag(tag.strip(),argv[1])
	else:#list all tags and allow user to select; print flist for selected tag
		tagDict=loadTagDict()
		tList=list( tagDict.keys() )
		tList.sort()
		printList(tList)
		choice=chooseFromList( tList )
		cfList=  getFilenameList(choice)
		printList(cfList)
		choice=chooseFromList( cfList)
		setClipboardData ( choice)
		
		
	

tagFile=r"C:\Users\Kevin\Util\resources\tagFile.txt"
#tagFile=r"C:\Users\Kevin\Util\resources\unitTests\tagFileTest.txt"