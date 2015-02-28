from os import listdir, system, chdir, getcwd, path
from root import screeningDir, standardizeFile, standardizeString, garbageBin
from copy import copy
from tag import tagMultipleFiles
from sys import exit as sys_exit
from shutil import move

#kept for reference
def __OBSOLETE_OLD_cleanNonAsciiChars(dirtyStr):
	cleaned=""
	for i in range(0,len(dirtyStr)):
		if(ord(dirtyStr[i])<128):
			cleaned="".join([cleaned,dirtyStr[i]])
	
	cleaned=cleaned.strip()
	
	return cleaned

#kept for reference	
def __OBSOLETE_OLD_CLEANFILENAMES(dir):
	
	fileList= listdir(dir)
	
	for i in range(0, len(fileList)):
		
		try:
			fileList[i].decode("ascii")
		
		except UnicodeDecodeError:
			newName=cleanNonAsciiChars(fileList[i]).strip()
			print "Renamed ", fileList[i], " to ", newName
			#system("".join(["rename \"",fileList[i],"\" \"",newName,"\""]))
			fileList[i]=newName
			
		try:
			
			newName=fileList[i].replace(("%7C"), "")
			newName=newName.replace(("%2A"), " ")
			newName=newName.replace(("&amp;"), "")
			newName=newName.replace(("&quot;"), "")
			newName=newName.replace("!","")
			while("  " in newName):
				newName=newName.replace(("  "), " ")
			
			if(newName[0]==" "):
				newName=newName[1:]
			
			if(fileList[i]!=newName):
				#system("".join(["rename \"",fileList[i],"\" \"",newName,"\""]))
				print "Renamed ", fileList[i], " to ", newName
				
		
		except ValueError:
			print "Value Error"
		
		#Special case to handle URL unicodes
		if( ("%8") in fileList[i] or ("%9") in fileList[i]):
			
			charList=[0,1,2,3,4,5,6,7,8,9,"A","B","C","D","E","F"]
			for j in range(0,len(charList)):
				percentConcat1="".join(["%8",str(charList[j])])
				percentConcat2="".join(["%9",str(charList[j])])
				try:
					newName=newName.replace(percentConcat1,"")
					newName=newName.replace(percentConcat2,"")
					
				except ValueError:
					print "Value Error"
				
			print "Renamed ", fileList[i], " to ", newName
			#system("".join(["rename \"",fileList[i],"\" \"",newName,"\""]))
		
		
		fixedEncodings=newName.encode('ascii','ignore')
		if(len(fixedEncodings)>0 and fixedEncodings!=newName):
			print "Final name: ", fixedEncodings
		#system("".join(["rename \"",newName,"\" \"",fixedEncodings,"\""]))
	
		


def deleteDuplicates(dir):
	#__VALID_EXT__=[".mp3",".mp4",".m4a", ".py", ".pyc", ".exe", ".bat", ".txt", ".c", ".cpp", ".lnk", ".java", ".bin", ".cmd", ".avi", ".mkv", ".m4v", ".rar", ".zip", ".msi",".mka"] KFR
	
	print "Deleting duplicates"
	
	fileList=listdir(dir)
	copiedList=copy(fileList)
	
	for i in range(0,len(fileList)):
		copiedList.remove(fileList[i])
		for j in range(0,len(copiedList)):
			
			if(fileList[i] in copiedList[j]):
				move(copiedList[j],garbageBin)
				
				

def screenTagging():
	"""Clean up filenames names and tags them with 'screen' tag"""
	
	chdir(screeningDir)
	if(getcwd()==screeningDir):
		print "Starting screen tagging"
		
		fileList=listdir(screeningDir)
		
		for i in range(0,len(fileList)):
			fileList[i]="".join([screeningDir,"\\",fileList[i]])
		
		#print fileList
		tagMultipleFiles(fileList,"screen")
	
	else:
		print "Wrong directory: Need screening directory"

		
	
def cleanFileNames(directory):
	
	fileList=listdir(directory)
	
	for i in range(len(fileList)-1,-1,-1):
		
		fileList[i]=standardizeFile(fileList[i])
		origFile=fileList[i]
		cleaned=cleanString(fileList[i])
		
		if(origFile!=cleaned):
	
			command="".join(["rename ","\"",directory,"\\",origFile,"\" \"",cleaned,"\""])
			
			
			if(system(command)==1):#if renaming fails, then file is deleted otherwise print output(success renaming)
				#system("del " + "\"" +origFile + "\"")
				#print "Deleted: ", origFile
				#fileList.remove(fileList[i])
				try:
					print "Moved to garbageBin: ", origFile
					move(origFile,garbageBin)
					fileList.remove(origFile)
				except IOError:
					print "Unable to move file", origFile
			else:
				output="".join(["Renamed: ", origFile , " to ",  cleaned])
				print output
			
def cleanChars(string):
	
	#assumption that string is already standardized 
	VALID_CHARS=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','0','1','2','3','4','5','6','7','8','9','.',' ','-', '(', ')','_','[',']','\'',',','#']
	
	cleaned=""
	
	string=string.replace(("&amp;"), "").replace(("&quot;"), "").replace('!','').replace('\"','').replace('&','').replace("\n","").strip()
	
	
	#reason for loop order:
	#	invalid chars can create multi spaces between words
	for i in range(0,len(string)):
		if(string[i]  in VALID_CHARS):
			cleaned="".join([ cleaned,string[i] ])
	
	while("  " in cleaned):	
		cleaned=cleaned.replace(("  "), " ")
	
	
	return cleaned
	
	
def cleanString(string):
	from os import path
	
	cleaned=cleanChars(string)
	extension=path.splitext(string)[1].replace('.','')
	
	try:
		while (cleaned[0]).isalnum()==False and cleaned[0]!='[':#>.>
			cleaned=cleaned[1:]
							
	except IndexError:
		print "Error: Cleaned file name is empty because it only consisted of non-alphanumeric characters."
		print "Original filename was: ", string
		cleaned=raw_input("Type new filename\n")
	
		
	if cleaned==extension:
		print "Error: Invalid cleaned file name. cleaned file name is equal to extension"
		print "Original filename was: ", string
		cleaned=raw_input("Type new filename\n")
		
	
	return cleaned


	
if __name__ == "__main__":
	from sys import argv
	
	if(len(argv)>1):	
		
		
		
		if(standardizeFile(argv[1])==standardizeFile(screeningDir)):
			#deleteDuplicates(screeningDir)
			cleanFileNames(argv[1])
			screenTagging()
	
		else:
			cleanFileNames(argv[1])
			
		
	else:
		print "Missing directory parameter"
	
	