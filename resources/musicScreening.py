from tag import getFilenameList, addTags, removeTags
from root import screeningDir, musicDir
from os import listdir, system, kill, path, rename, remove as os_remove
from string import lower
from msvcrt import kbhit, getch

from psutil import Process, get_pid_list, error
from shutil import move, Error as shutil_error
from sys import exit as sys_exit, argv
from time import sleep
from signal import SIGILL
from random import shuffle

def killVLC(tries=0):
	
	if tries<2:
		for pid in get_pid_list():
			try:
				if(Process(pid).name=="vlc.exe"):
					kill(pid, SIGILL)
			except error.NoSuchProcess:
				tries+=1
				killVLC(tries)
		
	else:
		raise Exception("VLC not found after 3 tries")
				

def pollForVLCExistance():
	procNameList=[ Process(pid).name for pid in  get_pid_list()  ]
	
	while "vlc.exe" not in procNameList:
		procNameList=[ Process(pid).name for pid in  get_pid_list()  ]
		sleep(0.5)


def getKeyPress(): 
    
	print "Type [k] to keep, [t] to keep and tag, [d] to delete track or [q] for quit"
	result=""
	#pollForVLCExistance()
	while (result==""):
        
		if kbhit():         
			result = (getch())
			inputChar=ord(result)
			if(inputChar==224 or inputChar==0):
				getch()
			
	result=lower(result)
	return result

def cutDir(fileName):	
	return path.split(fileName)[1]

def handleTagging(musicList, musicFileName, i):
	
	try:
		removeTags(["screen"], musicFileName)
		move(musicFileName,musicDir)
		
	except WindowsError:
		print "Failed to move file"
		print "Press enter to exit."
		addTags(["screen"],musicFileName)
		raw_input()
		sys_exit(1)

	except shutil_error:
		
		print "File already exists in main music directory"
		fileExt=path.splitext(musicFileName)[1]
		newMusicFileName=raw_input("Rename current music file:\n")
		while path.splitext(newMusicFileName)[1]!=fileExt:
			print "Invalid extension. Extension must be ", fileExt
			newMusicFileName=raw_input("Rename current music file:\n")
			
		tDir=path.split(musicFileName)[0]
		newMusicFileName="".join([tDir,"\\",newMusicFileName])
		rename(musicFileName, newMusicFileName)
		musicFileName=newMusicFileName
		
		move(musicFileName,musicDir)
		
		
	musicList.pop(i)
	
	filename="".join([musicDir,"\\",cutDir(musicFileName)])
	tagList=raw_input("Enter tag(s). Separate with commas\n").split(',')
	print ""
	addTags(tagList,filename)
	
def handleDelete(musicList, i):
	
	removeTags(["screen"], musicList[i].replace("\"",""))
	os_remove( musicList[i].replace("\"","") )
	if path.exists(musicList[i])==False: 
		print "Delete successful\n"
		musicList.pop(i)
	else:
		print "Failed to delete file"
		print "Press enter to exit."
		addTags(["screen"], musicList[i].replace("\"",""))
		raw_input()
		sys_exit(1)
	
def handleKeep(musicFileName, i):
	try:
		removeTags(["screen"], musicFileName.replace("\"",""))
		move(musicFileName,musicDir)
		
	except WindowsError:
		print "Failed to move file"
		print "Press enter to exit."
		addTags(["screen"],musicFileName.replace("\"",""))
		raw_input()
		sys_exit(1)
		
	except shutil_error:
		
		print "File already exists in main music directory"
		fileExt=path.splitext(musicFileName)[1]
		newMusicFileName=raw_input("Rename current music file:\n")
		while path.splitext(newMusicFileName)[1]!=fileExt:
			print "Invalid extension. Extension must be ", fileExt
			newMusicFileName=raw_input("Rename current music file:\n")
			
		tDir=path.split(musicFileName)[0]
		newMusicFileName="".join([tDir,"\\",newMusicFileName])
		rename(musicFileName, newMusicFileName)
		musicFileName=newMusicFileName
		
		
		move(musicFileName,musicDir)
			
	print "Move successful\n"
	musicList.pop(i)
	
def startScreening(musicList):
	
	quit=False
	for i in range(len(musicList)-1,-1,-1):
		
		if(quit==False):
		
			system( "".join(["\"",musicList[i],"\""]) )
			
			print "Playing: ", musicList[i]
			#system( "\"C:\\Program Files\\Rainmeter\\Rainmeter.exe\" !Refresh  Enigma\\Sidebar\\Music" ) # rid? rarely look at desktop anyway?
			
			prompt=getKeyPress()
			
			while all([prompt!="k", prompt!="d" , prompt!="t", prompt!="q"]):
				print "Invalid selection"
				prompt=getKeyPress()
				
			else:
				killVLC()
				musicFileName=musicList[i].replace("\"","")
				if(prompt=="k"):
					handleKeep(musicFileName, i)
					
				elif(prompt=="d"):
					handleDelete(musicList, i)
					
				elif(prompt=="t"):
					handleTagging(musicList, musicFileName, i)
					
				elif(prompt=="q"):
					quit=True
	
def loadMusic():
	
	musicList=getFilenameList(["screen"])
	
	#move from creation time sort to random
	shuffle(musicList)
	
	finalList=[]
	for i in range(0,len(musicList)):
		finalList.append("\"" + musicList[i] + "\"")

	return finalList
	

if __name__ == "__main__":
	
	musicList=loadMusic()
	
	if(len(musicList)>0):
		startScreening(musicList)
		
	else:
		print "No music to be screened available"
	
	
	