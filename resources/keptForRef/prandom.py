r""" 

Randomly plays x number of songs from given folder
-Default value for x is 30
-Number of songs can be changed
-Parameters can be changed to change VLC global hotkeys
-Extra tag parameters can be added to only play songs that match OR don't match the tags. 
	-Playing tags that don't match can be specified using '-'
	
USAGE: pRand [number of songs]/[tag]
[number of songs]: optional parameter
[tags]: optional parameter
"""

from random import randint
from ctypes import windll
from threading import Thread
from os import system, listdir, getenv, getcwd
from sys import exit as sys_exit, argv, stdin
from root import musicDir, switchBoard, compareLists, printNumberedList
from re import findall

AVAILABLE_SWITCHES=['v','h','#','e']
useMaxNumOfSongs=False
def getNumOfSongs(max):
	global argv
	
	numOfSongs=60#default_number
	
	if useMaxNumOfSongs==True:
		numOfSongs=max
	
	try:
		pos=[targ[0] for targ in switches].index('#')
		
		try:
			numOfSongs= int ( switches [pos][1])
		except ValueError:
			print "Invalid number with # switch. Terminating program."
			sys_exit(1)
		
	except:
		pass
		
		
	
	
	#if numOfSongs>max:
	#	numOfSongs=max
	
	
	return numOfSongs


	
def launch_VLC_Mode(switches):
	
	"""Launches VLC with the following controls if called by vlcBus.bat:
	
	Play/Pause:Z
	Vol Up/Down: Up arrow/Down arrow
	Previous song: Left arrow
	Next song: Right arrow
	
	"""
	
	if('b' in switches):
		system("start /MIN /B C:/\"Program Files (x86)\"/VideoLAN/VLC/vlc.exe --qt-start-minimized --one-instance --global-key-play-pause=z --global-key-vol-up=Up --global-key-vol-down=Down --global-key-prev=Left --global-key-next=Right --playlist-enqueue")
		
	elif('v' in switches):
		print "Launching in arrow key mode"
		#system(r"""start /B /MIN C:\"Program Files (x86)"\VideoLAN\VLC\vlc.exe --qt-start-minimized --one-instance --global-key-play-pause="Down" --global-key-prev="Left" --global-key-next="Right" --playlist-enqueue --playlist-autostart --playlist-enqueue""")
	
	
def getFolder():	
	"""
		Returns musicDir
	"""
	return musicDir
	
def getSongList(folder, exceptionTagList):
	from searchTags import getTagList, searchTags
	from root import standardizeString
	
	"""Returns list of songs obtained from folder
	
	-If tags are being used then function will call searchTags.searchTags(tagList) to return list of songs
	else list of songs is obtained by calling os.listdir(folder)
	
	-This method includes ALL the files from the directory/folder to the list
	The playSongs method is where it checks to only play the .mp3 files
	
	"""
	def concatFolder2(fileName):
		return "".join(["\"",fileName.strip(),"\""])		
	if len(argv)>1:
		
		tagList=getTagList(argv)
		songList=searchTags(tagList)
		global useMaxNumOfSongs
		useMaxNumOfSongs=True
		
		
		
		
	else:
		def concatFolder(fileName):
			return "".join(["\"",folder,"\\",fileName.strip(),"\""])
		songList=listdir(folder)
		songList=map(concatFolder,songList)
		
	
	if len(exceptionTagList)>0:
		carrier=[]
		exceptionSongList=[]
		exceptionTagList.insert(0,"placeHolder")
		exceptionTagList=getTagList(exceptionTagList)
		
		
		for exceptionTag in exceptionTagList:
			carrier.append(exceptionTag)
			
			exceptionSongList.extend( (searchTags( carrier ) ) )
			carrier=[]
			
		
		
		for i in range(len(songList)-1,-1,-1):
			
			if standardizeString(songList[i]) in exceptionSongList:
				songList.remove(songList[i])
			
		songList=map(concatFolder2,songList)#adds extra quotation marks to be able to play songs due to "&" char on emapth
		
		
		
		
	return songList
	

def playSongs(songList, folder, numOfSongs):
	from time import sleep
	"""Plays the songs from songList, from 0 upto numOfSongs
	
	Folder argument is used for concatenating to the beginning of song file if path is not given in the list
	Only plays songs from the list that contain ".mp3" in their filenames
	
	"""
	f=open("C:\\Users\\Kevin\\Util\\resources\\playback.txt","a")
	i, randNum = 0, 0
	
	
	while(i<numOfSongs):
		
		str=""
		
		
		randNum=randint(0, (len(songList)-1) )
		
		
		if(".mp3" in songList[randNum] or ".mka" in songList[randNum] or ".m4a" in songList[randNum]  or ".flac" in songList[randNum] or ".ogg" in songList[randNum]): #GENERALIZE THIS SHIT
			if( ("\"" in songList[randNum]) == False):
				str="".join(["\"",folder,"\\",songList[randNum],"\""])
				
			else:
				str=songList[randNum]		
				
			
			f.write(str+"\n")
			
			
		
		#Thread(target=system, args=(str,)).start()
		
		
		system(str.__str__())
		
		songList.pop(randNum)
		i+=1
		
	f.close()
	
	if("sleep," in argv):
		system("priority -n vlc")
		system("priority -l -e vlc")





if __name__ == "__main__":
	
	
	windll.kernel32.SetConsoleCtrlHandler(0, 1)
	
	if "-e" in argv:
		ePos=argv.index("-e")
		exceptionTagList=argv[ePos+1:]
		argv=argv[:ePos]
	else:
		exceptionTagList=[]
	
	
	
	switches=switchBoard(argv)
	
	
	
	if("h" in switches):
		print __doc__
		
	elif stdin.isatty()==False:
		#Purpose is for usage with nf
		#example: nf [files without tags but certain share common string in filename] -p | prand
		#using cwd
		print "Playing piped songs"
		rawInString=" ".join(map(str,stdin.readlines()))
		rawInString=rawInString[:rawInString.rindex("-------------------------------")]
		resultList=findall("\".+\.mka\"",rawInString)
		resultList.extend(findall("\".+\.m4a\"",rawInString))
		
		resultList.extend(findall("\".+\.mp3\"",rawInString))
		resultList.extend(findall("\".+\.flac\"",rawInString))
		resultList.extend(findall("\".+\.ogg\"",rawInString))
	
		#print rawInString
		#print resultList
		
		for i in range(0,len(resultList)):
			resultList[i]="".join(["\"",resultList[i],"\""])
		
		launch_VLC_Mode(switches)
		songList=resultList
		
		folder=getcwd()
		numOfSongs=(len(songList))
		
		
		playSongs(songList, folder, numOfSongs)
	
	else:
		
		folder=getFolder()
		
		songList=getSongList(folder,exceptionTagList)
		
		numOfSongs=getNumOfSongs(len(songList))
		#numOfSongs=getNumOfSongs(60)
		
		
		launch_VLC_Mode(switches)
		
		
		
		playSongs(songList, folder, numOfSongs)
		