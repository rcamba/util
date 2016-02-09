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



	unicodeToRomajiMapping={
		"\u3055" : "sa",
		"\u3044" : "i",
		"\u308f" : "wa",
		"\u3084" : "ya",
		"\u304b" : "ka",
		"\u306a" : "na",
		"\u671d" : "asa",
		"\u30e2" : "mo",
		"\u30ce" : "no",
		"\u7533" : "saru",
		"\u3059" : "su",
		"\u7dca" : "jin",
		"\u5f35" : "cho",
		"\u611f" : "kan",
		"\u51fa" : "de",
		"\u4f1a" : "kai",
		"\u697d" : "raku",
		"\u3057" : "shi",
		"\u306d" : "ne",
		"\u3047" : "e",
		"\u5c0f" : "ko",
		"\u7af6" : "keiri",
		"\u5408" : "go",
		"\u672c" : "hon",
		"\u266a" : "",
		"\u308a" : "ri",
		"\u6c17" : "ki",
		"\uff01" : "",
		"\u30e0" : "mu",
		"\u30c9" : "do",
		"\u52c7" : "yu",
		"\u6c17" : "ki",
		"\u306e" : " no ",
		"\u795e" : " kami",
		"\u69d8" : "sama ",
		"\u4e0a" : "jo",
		"\u54c1" : "hin",
		"\u3067" : "de ",
		"\u5feb" : "kai",
		"\u6d3b" : "katsu",
		"\u306a" : "na",
		"\u30b8" : "ji",
		"\u5a18" : "musume",
		"\u30ad" : "ki",
		"\u30ec" : "rete",
		"\u3066" : "te",
		"\u30d7" : "pu",
		"\u30f3" : "n",
		"\u30b9" : "su",
		"\uff01" : "",
		"\u30ab" : "ka",
		"\u732a" : "inoshishi ",
		"\u7a81" : "",
		"\u731b" : "mo",
		"\u9032" :  "suzumu",
		"\u8f9b" : "kara",
		"\u4e00" : "ichi",
		"\u751f" : "nama",
		"\u61f8" : "agata ",
		"\u547d" : "inochi",
		"\u611b" : "ai",
		"\u60c5" : "jo",
		"\u30ef" : "wa",
		"\u30bf" : "ta",
		"\u30b7" : "shi ",
		"\u30fb" : "",
		"\u611b" : "ai",
		"\u304a" : "o",
		"\u9858" : "gan",
		"\u2606" : "",
		"\u6fc0" : "geki",
		"\u9707" : "shin ",
		"\u30c0" : "da",
		"\u30b9" : "su",
		"\u30f4" : "vu",
		"\u30a3" : "ii",
		"\u30cb" : "ni",
		"\u30e3" : "ya",
		"\uff01" : "",
		"\u66b4" : "kyoiku ",
		"\u8650" : "joyo ",
		"\u7ffc" : "tsubasa",
		"\u5ca9" : "iwa",
		"\u584a" : "katamari ",
		"\u539f" : "gen",
		"\u91ce" : "no",
		"\u30d9" : "be",
		"\u30eb" : "ru",
		"\u30cf" : "ha",
		"\u30a4" : "i",
		"\u30d5" : "fu",
		"\u30a9" : "oo",
		"\u30eb" : "ru",
		"\u30bb" : "se",
		"\u30c6" : "te",
		"\u30a3" : "ii",
		"\u5927" : "dai",
		"\u901a" : "tsu",
		"\u6d6e" : "bo",
		"\u5cf6" : "shima",
		"\u8349" : "kusa",
		"\u30af" : "ku",
		"\u30ea" : "ri",
		"\u30f3" : "n",
		"\u30c7" : "de",
		"\u304f" : " ku",
		"\u9271" : "ko",
		"\u77f3" : "ishi",
		"\u30e9" : "ra",
		"\u30af" : "ku",
		"\u30bf" : "ta",
		"\u30c8" : "to",
		"\u30a2" : "a",
		"\u30c3" : "tsu",
		"\u30e7" : "yo",
		"\u7802" : "suna",
		"\u4e18" : "oka",
		"\u5ce1" : "kai",
		"\u8c37" : "tani ",
		"\u30a7" : "e",
		"\u30eb" : "ru",
		"\u30b0" : "gu",
		"\u30d8" :  "e",
		"\u7e1b" : "baku",
		"\u9396" : "kusari",
		"\u30a1" : "a",
		"\u30d6" : "su",
		"\u30e1" : "me",
		"\u5149" : "hikari",
		"\u3078" : "e",
		"\u604b" : "koi",
		"\u5b9d" : "takara",
		"\u7bb1" : "hako",
		"\u9759" : "sei",
		"\u708e" : "hono",
		"\u30bd" : "so",
		"\u84bc" : "ao",
		"\u6d99" : "namida",
		"\u30d2" : "hi",
		"\u30ca" : "na",
		"\u308b" : "ru",
		"\u60f3" : "so",
		"\u30a6" : "u",
		"\u8ffd" : "tsui",
		"\u61b6" : "oku",
		"\u679c" : "hate",
		"\u5b9f" : "mi",
		"\u672a" : "mi",
		"\u5b8c" : "kan",
		"\u6210" : "sei",
		"\u5730" : "ji",
		"\u56f3" : "zu",
		"\u30df" : "mi",
		"\u7d19" : "shi",
		"\u30b3" : "ko",
		"\u821e" : "mai",
		"\u3046" : "u",
		"\u5834" : "ba",
		"\u6240" : "sho",
		"\u3053" : "ko",
		"\u590f" : "natsu",
		"\u30b1" : "ke",
		"\u541b" : "kimi",
		"\u3068" : "to",
		"\u307e" : "ma",
		"\u8679" : "Niji",
		"\u8272" : "iro",
		"\u30e5" : "yu",
		"\u30d0" : "ba",
		"\u591c" : "Yoru",
		"\u5e83" : "Hiro",
		"\u304c" : "ga",
		"\u9752" : "Ao",
		"\u6625" : "haru",
		"\u661f" : "hoshi",
		"\u7a7a" : "sora",
		"\u30de" : "ma",
		"\u67d3" : "some",
		"\u307f" :  "mi",
		"\u7a4f" : "oda",
		"\u6642" : "toki",
		"\u3092" : "o",
		"\u6e21" : "watari ",
		"\u6301" : "ji",
		"\u3061" : "chi",
		"\u3070" : "ba",
		"\u3048" : "e",
		"\u624b" : "te",
		"\u80f8" : "mune",
		"\u9a12" : "sou",
		"\u304e" : "gi",
		"\u30aa" : "i",
		"\u65b0" : "Shin",
		"\u4e0d" : "fu",
		"\u610f" : "i",
		"\u6311": "cho",
		"\u767a" : "hatsu",
		"\u60b2" : "kanashii",
		"\u54c0" : " ai",
		"\u5b64" : "Ko",
		"\u9ad8" : "ko",
		"\u4eba" : "hito",
		"\u3054" : "go",
		"\u6a5f" : "ki",
		"\u5acc" : "iya",
		"\u3081" : "me",
		"\u71b1" : "netsu",
		"\u7684" : "teki",
		"\u81ea" : " ji ",
		"\u8aac" : "setsu",
		"\u5c55" : "ten",
		"\u958b" : " Hiraki",
		"\u3042" : "a",
		"\u3075" : "fu",
		"\u308c" : "re",
		"\u61d0" : "Futokoro ",
		"\u65e5" : "hi",
		"\u03a6" :  "",
		"\u5e0c" : "Nozomi ",
		"\u671b" : "mochi",
		"\u74b0" : "wa",
		"\\xb0" : "",
		"\u306b" : "ni",
		"\u305f" : "ta",
		"\u304b" : "ka",
		"\u3089" : "ra",
		"\u4e88" : "yo",
		"\u30ed" : "ro",
		"\u6708" : "Tsuki",
		"\u98df" : "shoku ",
		"\u6765" : "ki",
		"\u300c" : "",
		"\u597d" : "ko",
		"\u304d" : "ki",
		"\u3002" : "",
		"\u300d" : "",
		"\u8a00" : "gen",
		"\u5206" : "bun",
		"\u9593" : "kan",
		"\u5b66" : "gaku",
		"\u6821" : "ko"
	}


	for unicodeStr in unicodeToRomajiMapping.keys():
		word=word.replace(unicodeStr, unicodeToRomajiMapping[unicodeStr])


	if "\u3063" in word:
		word= word.replace("\u3063", word[word.index("\u3063")+1])

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
	tokens=path.splitext(cleaned)
	cleaned=tokens[0]
	cleaned=cleaned.strip()
	cleaned=cleaned+tokens[1]
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

		print key.encode("unicode_escape")+ " ---> " + changesDict[key]
		if 'p' not in switches: #if not printing only...
			try:
				rename(path.join(directory,key), path.join(directory,changesDict[key]))
			except WindowsError, e:
				errorAlert("Unable to rename " + key + " in to " + changesDict[key] +". Stopping program.")
				errorAlert(str(e))
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

	switches=switchParser(argv, AVAILABLE_SWITCHES)

	if(len(argv)>1):
		main(unicode(argv[1]))


	else:
		promptStr="\nClean filenames of current directory? [y]es / [n]o \n"
		choice=raw_input(promptStr).lower()
		while choice!='y' and choice!='n':
			print "Invalid choice: ", choice
			choice=raw_input(promptStr).lower()

		if choice=='y':
			#main(unicode(getcwd()))
			main(u'.')

