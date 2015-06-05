from os import path, getcwd, listdir, chdir
from root import errorAlert, removedFilesLog, chooseFromList, printList, createBackUp, setClipboardData, tagFile, tagFilesLogDir
from string import rstrip, lower, strip
from re import findall
from collections import OrderedDict
from sys import argv
from threading import Thread

import inspect

def _splitTagFile():#init -one time
	chdir(tagFilesLogDir)
	tagDict=loadTagDict()

	for key in tagDict.keys():
		fileList=tagDict[key]
		writer=open(key+".tag",'wb')
		writer.write(key)
		writer.write("::")
		for file in fileList:
			writer.write("\""+file+"\"")
			writer.write(" ")
		writer.close()

def reconstructTagDict():
	fList=listdir(tagFilesLogDir)
	rTagDict={}
	for f in fList:
		reader=open(path.join(tagFilesLogDir,f),'rb')
		line=reader.read()#each file only has one line
		tag, fileStringList=line.split('::')
		tagFileList=convertToFilenameList(fileStringList)
		rTagDict[tag]=tagFileList
		reader.close()

	return rTagDict

def setTagFile(newTagFile=r"C:\Users\Kevin\Util\resources\unitTests\tagFileTest.txt", newLogsDir=r"c:\users\kevin\util\resources\unitTests\tagLogsTest"):#for testing
	global tagFile
	global tagLogsDir
	tagFile=newTagFile
	tagLogsDir=newLogsDir

def logRemovedFile(msg):
	writer=open(removedFilesLog,'a')
	writer.write(msg)
	writer.close()

def validateFilename(filename, assocTag=""):
	validFileList=validateFilenameList( filename, assocTag )
	res=""
	if len(validFileList)==1:
		res=validFileList[0]

	return res

def validateFilenameList(filenameList, assocTag=""):

	origFlist=filenameList
	if type(origFlist)==str:
		file=filenameList

		filenameList=[]
		filenameList.append(file)

	validFileList=[]

	for file in filenameList:

		if path.isabs(file)==False:
			file=getcwd()+'\\'+file


		if path.isfile(file)==False:
			if inspect.stack()[1][3]=="addTags":# caller methodName
				msg=errorAlert("Unable to add to tag " + assocTag + ". "+ file + " is an invalid file. ")
			elif inspect.stack()[1][3]=="loadTagDict":
				msg=errorAlert(file + " is an invalid file. Removed from "+ assocTag +" tag.")
			else:
				msg=errorAlert("Removed invalid file " + file)
			logRemovedFile(msg)

		else:
			validFileList.append(lower(file))

	return validFileList

def addTags(tagList, filename):

	for tag in tagList:
		tag=lower(tag).strip()

		validatedFilename=validateFilename(filename, tag)
		if len(validatedFilename)>0:
			tagDict=loadTagDict()

			if tagDict.has_key(tag):

				if len(tagDict[tag])!=len(set(tagDict[tag])) or validatedFilename in tagDict[tag]:#check for duplicates i.e tag already has file in its filelist
					duplicateList= list (set([x for x in tagDict[tag] if tagDict[tag].count(x) > 1]) )

					if len(duplicateList)==0:#adding existing filename into tag
						duplicateList=[validatedFilename]

					for d in duplicateList:
						errorAlert(validatedFilename + " already has tag: "+ tag)
				else:
					tagDict[tag].append(validatedFilename)

				#tagDict[tag]= list(set(tagDict[tag])) #remove files in same tag
			else:
				tagDict[tag]=[validatedFilename]
				print "Creating new tag: ", tag


			__writeTagFile__(tagDict)

		else:
			errorAlert( "No valid file to add. No changes have been made")

def tagMultipleFiles(tag, filenameList):

	validFileList=validateFilenameList(filenameList, tag)
	if len(validFileList)>0:
		tagDict=loadTagDict()

		if tagDict.has_key(tag):
			tagDict[tag].extend(validFileList)
			if len(tagDict[tag])!=len(set(tagDict[tag])):#check for duplicates i.e tag already has file in its filelist
				duplicateList= list (set([x for x in tagDict[tag] if tagDict[tag].count(x) > 1]) )

				for d in duplicateList:
					errorAlert(d + " already has tag: "+ tag)

			tagDict[tag]= list(set(tagDict[tag])) #remove files in same tag
		else:
			tagDict[tag]=validFileList
			print "Creating new tag: ", tag



		__writeTagFile__(tagDict)

	else:
		errorAlert( "No valid file to add. No changes have been made")

def removeTags(tagList, filename):

	changes=False
	validatedFilename=validateFilename(filename)
	if len(validatedFilename)>0:
		tagDict=loadTagDict()
		for tag in tagList:
			tag=lower(tag).strip()
			if tagDict.has_key(tag):
				try:
					tagDict[tag].remove(validatedFilename)
					changes=True
					print "Successfully removed " + validatedFilename + " from tag: ", tag

				except ValueError:
					errorAlert("Tag:" + tag + " doesn't have filename : " + validatedFilename + "\nNo changes have been made.")

			else:
				errorAlert( "Tag: " + tag + " doesn't exist.")

		if changes==True:

			__writeTagFile__(tagDict)

	else:
		errorAlert( "Invalid file. No changes have been made.")



def __writeTagFile__(changesDict, mode):

	"""
	mode:
		w -- re-write entire tag file-> used for removing tags
		a -- append to tag file -> used for adding tags
	"""

	for key in changesDict.keys():
		tagFile=path.join(tagFilesLogDir, key+".tag")
		createBackUp( tagFile, path.join(backUpDir, "tagFile") )
		writer=open(tagFile,mode)

		fileList= changesDict[key]
		writer.write(key)
		writer.write(key+"::")
		for file in fileList:
			writer.write("\"" + lower(file) + "\" ")

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
		#list( set ( validFileList) ) #force rid of duplicates...

		if len(filenameList)!=len(validFileList): #changes to filelist: a file was removed
			changes=True

	if changes==True:
		print "Updating changes when loading dictionary"
		__writeTagFile__(tagDict)

	return tagDict

def getFilenameList(tagList):#str or list
	if type(tagList)==str:
		tagList=[tagList]

	tagDict=loadTagDict()

	result=[]

	counter=0
	tagList=map(lower,tagList)
	for tag in tagList:
		if tagDict.has_key(tag):
			if counter>0:
				result=list(set(tagDict[tag]).intersection(set(result)))
			else:
				result.extend(tagDict[tag])
		else:
			errorAlert("Tag doesn't exist: " + tag)
		counter=counter+1

	return result



def getTagList(filename=""):
	tagDict=loadTagDict()

	if len(filename)==0:
		tagList= tagDict.keys()
	else:
		tagList=[]
		filename=validateFilename(filename)
		for key in tagDict.keys():
			if filename in tagDict[key]:
				tagList.append(key)

	return tagList

def getMixedFilenameList(tagList):#for prand
	res=[]
	for tag in tagList:
		res.extend(getFilenameList(tag))
	res=list(set(res))
	return res

if __name__=="__main__":


	if len(argv)>1:
		tagList=raw_input("Enter tag(s). Separate with commas\n").split(',')



		addTags(tagList,argv[1])
	else:
		print "Missing args"
