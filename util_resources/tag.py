from os import path, getcwd, listdir, remove as removeFile
from root import error_alert, removed_files_log, create_back_up,  tag_files_log_dir, backup_dir, piped_list, key_press_input
from string import lower, strip
from re import findall
from sys import argv, stdin
from threading import Thread
from fnmatch import translate
import re
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
def _rtd(f, rTagDict, changesDict):
	with open(path.join(tag_files_log_dir, f), 'rb') as reader:
		line=reader.read()#each file only has one line

	tag, fileStringList=line.split('::')
	filenameList=convertToFilenameList(fileStringList)

	validFileList=validateFilenameList(filenameList, tag)
	rTagDict[tag]=validFileList

	if len(filenameList)!=len(validFileList): #changes to filelist: a file was removed
		changesDict[tag]=validFileList

def reconstructTagDict():

	fList=listdir(tag_files_log_dir)
	rTagDict={}
	tList=[]

	changesDict={}
	for f in fList:
		tList.append(Thread(target=_rtd, args=(f,rTagDict,changesDict)))
		tList[len(tList)-1].start()

	for t in tList:
		t.join()

	if len(changesDict)>0:
		print "Updating changes when loading dictionary"
		print "Tags to be updated: " + str(changesDict.keys())
		__writeTagFile__(changesDict, 'w')

	return rTagDict


def logRemovedFile(msg):
	with open(removed_files_log, 'a') as writer:
		writer.write(msg)
		writer.write('\n')

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
				msg=error_alert("Unable to add to tag " + assocTag + ". " + file + " is an invalid file. ")
			elif inspect.stack()[1][3]=="_rtd":
				msg=error_alert(file + " is an invalid file. Removed from " + assocTag + " tag.")

			else:
				msg=error_alert("Removed invalid file " + file)
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
			tagFilesList=listdir(tag_files_log_dir)
			tagFilesList=[ path.splitext(t)[0] for t in tagFilesList]

			if tag in tagFilesList:
				with open(path.join(tag_files_log_dir, tag+ ".tag")) as  r:
					tagFileLine=r.read()
				tag, fileStringList=tagFileLine.split('::')
				filenameList=convertToFilenameList(fileStringList)

				if validatedFilename in filenameList:#check if tag already has file in its filelist
					error_alert(validatedFilename + " already has tag: " + tag)
				else:
					if changesDict.has_key(tag):
						changesDict[tag].extend([validatedFilename])
					else:
						changesDict[tag]=[validatedFilename]
			else:
				print "Creating new tag: ", tag

				changesDict[tag]=[validatedFilename]

		else:
			error_alert("Unable to tag invalid file: " + filename)

	__writeTagFile__(changesDict,'a')

def tagMultipleFiles(tag, filenameList):

	validFileList=validateFilenameList(filenameList, tag)
	if len(validFileList)>0:
		for file in validFileList:
			addTags([tag], file)

	else:
		error_alert("No valid file to add. No changes have been made")

def removeTags(tagList, filename, validate=True):

	changesDict={}
	validatedFilename = filename
	if validate:
		validatedFilename = validateFilename(filename)
	if len(validatedFilename)>0:

		for tag in set(tagList):
			tag=lower(tag).strip()

			try:
				with open(path.join(tag_files_log_dir, tag+ ".tag")) as r:
					tagFileLine=r.read()
				tag, fileStringList=tagFileLine.split('::')
				filenameList=convertToFilenameList(fileStringList)

				if validatedFilename in filenameList:
					filenameList.remove(validatedFilename)
					changesDict[tag]=filenameList
					print "Successfully removed " + validatedFilename + " from tag: " + tag

				else:
					error_alert("Tag:" + tag + " doesn't have filename : " + validatedFilename + "\nNo changes have been made.")

			except IOError:
				error_alert("Tag file: " + tag + ".tag doesn't exist.")

		__writeTagFile__(changesDict,'w')

	else:
		error_alert("Invalid file. No changes have been made.")


def __writeTagFile__(changesDict, mode):
	"""
	mode:
		w -- re-write entire tag file-> used for removing tags
		a -- append to tag file -> used for adding tags
	"""
	if (mode=='a' or mode=='w')==False:
		raise ValueError("mode must be either 'a' or 'w'")

	origMode=mode

	for key in changesDict.keys():
		tagFile=path.join(tag_files_log_dir, key + ".tag")

		if path.exists(tagFile):
			create_back_up(tagFile, path.join(backup_dir, "tagFile"))
			if origMode=='a':
				mode='a'
		else:
			mode='w'
			print "Mode set to 'w' for: "  + key
			print "Number of files: " + str(len(changesDict[key])) + "\n"

		with open(tagFile,mode) as writer:

			fileList= changesDict[key]

			if len(fileList)>0:
				if mode=='w':
					writer.write(key+"::")

				for file in fileList:
					writer.write("\"" + lower(file) + "\" ")

		with open(tagFile) as reader:
			content=reader.read()

		if len(content)==0:
			msgLog="Empty file list. Removing tag :" + key
			error_alert(msgLog)
			logRemovedFile(msgLog)
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
			error_alert("Tag doesn't exist: " + tag)
		counter=counter+1

	return result


def getTagList(filename=""):
	tagDict=reconstructTagDict()
	#USE THREADING IN reconstructTagDict implement here
	#check efficiency saved
	#also do the thing with POPEN on VLC when pranding...
	if len(filename)==0:
		tagList= tagDict.keys()
	else:
		tagList=[]
		filename=validateFilename(filename)
		tagList=[key for key in tagDict.keys() if filename in tagDict[key]]

	return tagList

def getMixedFilenameList(tagList):#for prand + search
	result=[]
	tagDict=reconstructTagDict()

	tagList=map(lower,tagList)
	for tag in tagList:
		if tagDict.has_key(tag):
			result.extend(tagDict[tag])
		else:
			error_alert("Tag doesn't exist: " + tag)

	result=list(set(result))

	return result

def regexGetTag(argList):
	res=[]
	tList=getTagList()

	#res.extend([tag for tag in tList if arg in tag])

	#pattern=translate(" ".join(argList))
	pattern=(" ".join(argList))
	print pattern
	reObj=re.compile(pattern)
	for tag in tList:
		match=reObj.findall(tag)
		if len(match)>0:
			res.append(tag)


	return res

def handleTagSwitch(switch, **kwargs):
	if switch=="e": #exception
		pass
	elif switch=="r": #regex
		print kwargs
		return regexGetTag(kwargs["argList"])
	elif switch=="m": #mixed
		pass
	elif switch=="": #
		pass

if __name__=="__main__":

	if len(argv)>1:
		tagList=raw_input("Enter tag(s). Separate with commas\n").split(',')

		addTags(tagList,argv[1])

	elif stdin.isatty()==False:#for using with nf/search
		print "Tagging pipes"
		fileList=piped_list("".join(map(str, stdin.readlines())))
		tagList=key_press_input("Enter tag(s). Separate with commas").split(',')
		for tag in tagList:
			tagMultipleFiles(tag, fileList)
	else:
		print "Missing args"