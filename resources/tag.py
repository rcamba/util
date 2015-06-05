from os import path, getcwd, listdir, chdir, remove as removeFile
from root import errorAlert, removedFilesLog, chooseFromList, printList, createBackUp, setClipboardData, tagFilesLogDir, backUpDir
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
		reader.close()

		tag, fileStringList=line.split('::')
		filenameList=convertToFilenameList(fileStringList)
		validFileList=validateFilenameList(filenameList, tag)
		rTagDict[tag]=validFileList

		if len(filenameList)!=len(validFileList): #changes to filelist: a file was removed
			changesDict={}
			changesDict[tag]=validFileList
			print "Updating changes when loading dictionary"
			__writeTagFile__(changesDict, 'w')

	return rTagDict


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
			elif inspect.stack()[1][3]=="reconstructTagDict":
				msg=errorAlert(file + " is an invalid file. Removed from "+ assocTag +" tag.")
			else:
				msg=errorAlert("Removed invalid file " + file)
			logRemovedFile(msg)

		else:
			validFileList.append(lower(file))

	return validFileList

def addTags(tagList, filename):
	changesDict={}
	for tag in tagList:
		tag=lower(tag).strip()

		validatedFilename=validateFilename(filename, tag)
		if len(validatedFilename)>0:
			tagFilesList=listdir(tagFilesLogDir)
			tagFilesList=[ path.splitext(t)[0] for t in tagFilesList]

			if tag in tagFilesList:
				tagFileLine=open( path.join(tagFilesLogDir, tag+".tag") ).read()
				tag, fileStringList=tagFileLine.split('::')
				filenameList=convertToFilenameList(fileStringList)
				if validatedFilename in filenameList:#check if tag already has file in its filelist
					errorAlert(validatedFilename + " already has tag: "+ tag, raiseException=True)
			else:
				print "Creating new tag: ", tag

			changesDict[tag]=[validatedFilename]

			__writeTagFile__(changesDict,'a')

		else:
			errorAlert( "Unable to tag invalid file: " + filename)

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

		if path.exists(tagFile):
			createBackUp( tagFile, path.join(backUpDir, "tagFile") )
		else:
			mode='w'

		writer=open(tagFile,mode)

		fileList= changesDict[key]
		if len(fileList)>0:
			if mode=='w':
				writer.write(key+"::")

			for file in fileList:
				writer.write("\"" + lower(file) + "\" ")

		writer.close()

		reader= open(tagFile)
		content=reader.read()
		reader.close()
		if len(  content )==0:
			print "Empty file list. Removing tag :", key
			removeFile(tagFile)


def convertToFilenameList(fileStringList):
	res=[]

	fileStringList=findall('".+?"', fileStringList)

	for fileStr in fileStringList:
		res.append( fileStr.replace('\"','') )

	return res

def loadTagDict():
	return reconstructTagDict()
	"""
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
	"""
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
