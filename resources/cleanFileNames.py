from os import listdir, chdir, getcwd, path, rename, sep
from root import screeningDir, standardizeFile, errorAlert, switchParser
from tag import tagMultipleFiles, getFilenameList
from sys import argv, exit as sys_exit
from string import ascii_letters, digits

AVAILABLE_SWITCHES=['p']

def screenTagging():
	"""Clean up filenames names and tags them with 'screen' tag"""

	chdir(screeningDir)
	if(getcwd()==screeningDir):
		print "Starting screen tagging"

		fileList=listdir(screeningDir)
		screeningList=getFilenameList("screen")
		removedCounter=0
		for i in range(len(fileList)-1,-1,-1):
			fileList[i]="".join([screeningDir,sep,fileList[i]]).lower()

			if fileList[i] in screeningList:
				#print fileList[i], " already has screen tag"
				fileList.remove(fileList[i])
				removedCounter=removedCounter+1

		tagMultipleFiles("screen",fileList)
		print removedCounter, " songs already had screen tag"
		print "Tagged ", len(fileList), " files"


	else:
		print "Wrong directory: Need screening directory"


def cleanFileNames(directory):

	fileList=listdir(directory)
	changesDict={}

	for i in range(len(fileList)-1,-1,-1):

		#fileList[i]=standardizeFile(fileList[i])

		cleaned=cleanString(fileList[i])

		if(fileList[i]!=cleaned):
			changesDict[fileList[i]]=cleaned

	return changesDict

def cleanChars(dirtyStr):
	VALID_CHARS=list(ascii_letters) + list(digits) + ['.',' ','-', '(', ')','_','[',']','\'',',','#','~']

	cleaned=""

	#clean invalid chars
	for i in range(0,len(dirtyStr)):
		if(dirtyStr[i]  in VALID_CHARS):
			cleaned="".join([cleaned,dirtyStr[i] ])

	#clean extra spaces
	cleaned=cleaned.strip()
	while("  " in cleaned):
		cleaned=cleaned.replace(("  "), " ")

	#char must start either alphanumeric or with '['
	while len(cleaned)>0 and cleaned[0].isalnum()==False and cleaned[0]!='[':
		cleaned=cleaned[1:]

	return cleaned


def cleanString(dirtyStr, testOutput=None):
	cleaned=cleanChars(dirtyStr)

	token=path.splitext(cleaned)
	fn_only=token[0]

	if (len(cleaned)>0 and len(fn_only)>0)==False :#cleaned==0 is possible if file has no extension

		out="Error: Cleaned filename is empty because it only consisted of non-alphanumeric characters."
		errorAlert( out )

		if type(testOutput)==list:
			testOutput.append(out)
			cleaned="pass.test"

		else:
			print "Original filename was: ", dirtyStr
			cleaned=raw_input("Type new filename\n")

	return cleaned


def renameFiles(changesDict, directory):
	if 'p' in switches: #print only
		print  "Printing only. No changes will be made"

	for key in changesDict.keys():

		print key + " ---> " + changesDict[key]
		if 'p' not in switches: #if not printing only...
			try:
				rename(path.join(directory,key), path.join(directory,changesDict[key]))
			except WindowsError:
				errorAlert("Unable to rename " + key + " in to " + changesDict[key] +". Stopping program.")
				sys_exit(1)


def main(directory):
	if path.isdir(directory):

		changesDict=cleanFileNames(directory)
		renameFiles(changesDict, directory)

		if(standardizeFile(directory)==standardizeFile(screeningDir)):
			if 'p' not in switches:
				screenTagging()
	else:
		errorAlert("Argument must be a valid directory")

if __name__ == "__main__":

	switches=switchParser(argv)

	if(len(argv)>1):
		main(argv[1])


	else:
		promptStr="\nClean filenames of current directory? [y]es / [n]o \n"
		choice=raw_input(promptStr).lower()
		while choice!='y' and choice!='n':
			print "Invalid choice: ", choice
			choice=raw_input(promptStr).lower()

		if choice=='y':
			#main(getcwd())
			main(u'.')

