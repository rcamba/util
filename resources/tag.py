from os import path, getcwd, listdir, remove as removeFile
from root import errorAlert, removedFilesLog, createBackUp,  tagFilesLogDir, backUpDir
from string import lower, strip
from re import findall
from sys import argv
from threading import Thread

import inspect

"""
def _splitTagFile():#init -one time
	chdir(tagFilesLogDir)
	tagDict=reconstructTagDict()

	for key in tagDict.keys():
		fileList=tagDict[key]
		writer=open(key+".tag",'wb')
		writer.write(key)
		writer.write("::")
		for file in fileList:
			writer.write("\""+file+"\"")
			writer.write(" ")
		writer.close()
"""
def _rtd(f, rTagDict):
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

def reconstructTagDict():

	fList=listdir(tagFilesLogDir)
	rTagDict={}
	tList=[]
	for f in fList:
		#_rtd(f,rTagDict)
		tList.append(Thread(target=_rtd, args=(f,rTagDict)))
		tList[len(tList)-1].start()

	for t in tList:
		t.join()

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
	for tag in set(tagList):
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
					errorAlert(validatedFilename + " already has tag: "+ tag)
				else:
					if changesDict.has_key(tag):
						changesDict[tag].extend([validatedFilename])
					else:
						changesDict[tag]=[validatedFilename]
			else:
				print "Creating new tag: ", tag

				changesDict[tag]=[validatedFilename]

		else:
			errorAlert( "Unable to tag invalid file: " + filename)

	__writeTagFile__(changesDict,'a')

def tagMultipleFiles(tag, filenameList):

	validFileList=validateFilenameList(filenameList, tag)
	if len(validFileList)>0:
		for file in validFileList:
			addTags([tag], file)

	else:
		errorAlert( "No valid file to add. No changes have been made")

def removeTags(tagList, filename):

	changesDict={}
	validatedFilename=validateFilename(filename)
	if len(validatedFilename)>0:

		for tag in set(tagList):
			tag=lower(tag).strip()

			try:
				tagFileLine=open( path.join(tagFilesLogDir, tag+".tag") ).read()
				tag, fileStringList=tagFileLine.split('::')
				filenameList=convertToFilenameList(fileStringList)

				if validatedFilename in filenameList:
					filenameList.remove(validatedFilename)
					changesDict[tag]=filenameList
					print "Successfully removed " + validatedFilename + " from tag: " + tag

				else:
					errorAlert("Tag:" + tag + " doesn't have filename : " + validatedFilename + "\nNo changes have been made.")

			except IOError:
				errorAlert( "Tag file: " + tag + ".tag doesn't exist.")

		__writeTagFile__(changesDict,'w')

	else:
		errorAlert( "Invalid file. No changes have been made.")


def __writeTagFile__(changesDict, mode):
	"""
	mode:
		w -- re-write entire tag file-> used for removing tags
		a -- append to tag file -> used for adding tags
	"""
	if (mode=='a' or mode=='w')==False:
		raise ValueError("mode must be either 'a' or 'w'")

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


def getFilenameList(tagList):#str or list
	if type(tagList)==str:
		tagList=[tagList]

	tagDict=reconstructTagDict()

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
	tagDict=reconstructTagDict()

	if len(filename)==0:
		tagList= tagDict.keys()
	else:
		tagList=[]
		filename=validateFilename(filename)
		tagList=[key for key in tagDict.keys() if filename in tagDict[key]]

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