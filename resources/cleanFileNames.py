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

def unicodeToRomaji(word):

	word=word.replace("\u3044","i").replace("\u30e0","mu").replace("\u30c9","do").replace("\u3055","sa").replace("\u308f","wa").replace("\u3084","ya").replace("\u304b","ka").replace("\u306a","na").replace("\u671d","asa").replace("\u30e2","mo").replace("\u30ce","no").replace("\u7533","saru").replace("\u3059","su").replace("\u7dca","jin").replace("\u5f35","cho").replace("\u611f","kan").replace("\u51fa","de").replace("\u4f1a","kai").replace("\u697d","raku").replace("\u3057","shi").replace("\u306d","ne").replace("\u3047","e").replace("\u5c0f","ko").replace("\u7af6","keiri").replace("\u5408","go").replace("\u672c","hon").replace("\u266a","").replace("\u308a","ri").replace("\u6c17","ki").replace("\uff01","").replace("\u5909","hen").replace("\u5e7b","maboroshi ").replace("\u81ea","ji").replace("\u5728","zai").replace("\u306e","no").replace("\u30de","ma").replace("\u30b8","ji").replace("\u30ab","ka").replace("\u30eb","ru").replace("\u30b9","su").replace("\u30bf","ta").replace("\u7d76","ze").replace("\u9802","tsuitadaki").replace("\u30dd","po").replace("\u30a4","i").replace("\u30ba","zu").replace("\u30f3","n").replace("\u541b","kimi").replace("\u3092","o").replace("\u5f85","machi").replace("\u3064","tsu").replace("\uff1a00","").replace("\u201c","").replace("\u201d","").replace("\u6708","tsuki").replace("\u306e","no").replace("\u7ffc","tsubasa")

	if "\u30fc" in word:
		word= word.replace("\u30fc", word[word.index("\u30fc")-1])

	return word

def cleanFileNames(directory):

	fileList=listdir(directory)
	changesDict={}

	for i in range(len(fileList)-1,-1,-1):

		#fileList[i]=standardizeFile(fileList[i])

		cleaned=cleanString(fileList[i])

		if(fileList[i]!=cleaned):
			print "added", fileList[i].encode("unicode_escape")
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
	dirtyStr=dirtyStr.encode("unicode_escape")
	dirtyStr=unicodeToRomaji(dirtyStr)

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

