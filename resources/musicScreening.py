from tag import getFilenameList, addTags, removeTags
from root import screeningDir, musicDir, addMember
from os import listdir, system, stat, kill, path, rename
from string import lower
from msvcrt import kbhit, getch
from psutil import Process, get_pid_list
from shutil import move, Error as shutil_error
from sys import exit as sys_exit, argv
from time import sleep
from signal import SIGILL
from random import shuffle


def killVLC():
	for pid in get_pid_list():
		try:
			if(Process(pid).name=="vlc.exe"):#launch vlc ourselves so we know it's PID?
				kill(pid, SIGILL)

		except:
			pass
			
	sleep(0.3)
	
def getKeyPress(): 
    
	print "Type [k] to keep, [t] to keep and tag, [d] to delete track or [q] for quit"
	result=""
	while (result==""):
        
		#if kbhit():         
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
		#removed second handling of WindowsError...
		
	musicList.pop(i)
	
	
	
	filename="".join([musicDir,"\\",cutDir(musicFileName)])
	tagList=raw_input("Enter tag(s). Separate with commas\n").split(',')
	print ""
	addTags(tagList,filename)
	
	
def handleDelete(musicList, i):
	
	removeTags(["screen"], musicList[i].replace("\"",""))
	command="".join(["del ",musicList[i]])
	system(command)
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
			
			while(prompt!="k" and prompt!="d" and prompt!="t" and prompt!="q"):
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
	
	
	i=len(musicList)-1
	
	while(i>-1):
		
		musicList[i]=addMember(musicList[i].replace("\"",""),stat)
		i=i-1
	
	#morphedList=sorted(musicList, key=lambda Metamorph:Metamorph.getAttribute().st_ctime)
	#move from creation time sort to random
	shuffle(musicList)
	morphedList=musicList
	
	finalList=[]
	for i in range(0,len(morphedList)):
		finalList.append("".join(["\"",morphedList[i].getObject(),"\""]))
	
	finalList.reverse()
	return finalList
	

if __name__ == "__main__":
	
	musicList=loadMusic()
	
	if(len(musicList)>0):
		startScreening(musicList)
		
	else:
		print "No music to be screened available"
	
	
	