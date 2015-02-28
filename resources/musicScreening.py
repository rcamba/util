from tag import getFilenameList, addTag
from root import screeningDir, musicDir, addMember, switchBoard
from os import listdir, system, stat, kill, path, rename
#from operator import itemgetter, attrgetter - Not sure what this was initially used for?
from string import lower
from msvcrt import kbhit, getch
from psutil import Process, get_pid_list
from shutil import move, Error as shutil_error
from sys import exit as sys_exit, argv
from threading import Thread
from time import sleep
from signal import SIGILL

from prandom import launch_VLC_Mode




AVAILABLE_SWITCHES=['v']

filesInDir=map(lower,listdir(screeningDir))
verNum=1.4

def killVLC():
	#KILLSIG=9
	
	for pid in get_pid_list():
		try:
			if(Process(pid).name=="vlc.exe"):
				kill(pid, SIGILL)

		except:
			pass
			
	sleep(0.3)
	
def reverseSlash(string):
	reversed=string.replace("/","\\")

	return reversed
	
def replaceScreenTag(fileList):#CONSIDER USING tagMultipleFiles instead 
	
	existingTagList=loadTagFile()
	i=0
	while(i<len(existingTagList)):
		if(str(existingTagList[i].getTag())=="screen"):
			existingTagList[i].setFileList(fileList)
			i=len(existingTagList)
		i=i+1
	
	writeToFile(existingTagList,"w")
			
def getKeyPress(): 
    
	print "Type [k] to keep, [t] to keep and tag, [d] to delete track or [q] for quit\n"
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
	
	newFileName=""
	
	newFileName=path.split(fileName)[1]
	
	return newFileName

def startScreening(musicList):
	
	quit=False
	for i in range(len(musicList)-1,-1,-1):
		
		if(quit==False):
			if('v' in switches):
				launch_VLC_Mode(switches)
			system( "".join(["\"",musicList[i],"\""]) )
			#Thread(target=system, args=(str(musicList[i]),)).start()
			
			print "Playing: ", musicList[i]
			system( "\"C:\\Program Files\\Rainmeter\\Rainmeter.exe\" !Refresh  Enigma\\Sidebar\\Music" )
			
			prompt=getKeyPress()
			
			while(prompt!="k" and prompt!="d" and prompt!="t" and prompt!="q"):
				print "Invalid selection"
				prompt=getKeyPress()
				
			else:
				killVLC()
				musicFileName=musicList[i].replace("\"","")
				if(prompt=="k"):
					#command="".join(["move ",reverseSlash(musicList[i])," \"",reverseSlash(musicDir),"\""])
					#system("".join(["nF /d ",musicDir]))
					#kept for reference
					try:
						move(musicFileName,musicDir)
						
					except WindowsError:
						print "Failed to move file"
						print "Press enter to exit."
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
						
						try:
							move(musicFileName,musicDir)
							
						except WindowsError:
							print "Failed to move file"
							print "Press enter to exit."
							raw_input()
							sys_exit(1)
							
					print "Move successful"
					musicList.pop(i)
					
				elif(prompt=="d"):
					command="".join(["del ",musicList[i]])
					system(command)
					if path.exists(musicList[i])==False:
						print "Delete successful"
						musicList.pop(i)
					else:
						print "Failed to delete file"
						print "Press enter to exit."
						raw_input()
						sys_exit(1)
					
					
				
				elif(prompt=="t"):
					
					try:
						move(musicFileName,musicDir)
						
					except WindowsError:
						print "Failed to move file"
						print "Press enter to exit."
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
						
						try:	
							move(musicFileName,musicDir)
							
						except WindowsError:
							print "Failed to move file"
							print "Press enter to exit."
							raw_input()
							sys_exit(1)
						
					musicList.pop(i)
					fileName="".join(["\"",musicDir,"\\",cutDir(musicFileName),"\""])
					
					tagList=raw_input("Enter tag(s):\n").split(',')
					for tag in tagList:
						addTag(tag,[fileName])
					
					
					
				elif(prompt=="q"):
					quit=True
				
				
	
	replaceScreenTag(musicList)
	
	

	
def loadMusic():
	
	musicList=getFilenameList(["screen"])
	#musicList=searchTags(["psyscreen"])
	
	i=len(musicList)-1
	
	while(i>-1):
		
		musicList[i]=addMember(musicList[i].replace("\"",""),stat)
		i=i-1
	
	musicList=sorted(musicList, key=lambda Metamorph:Metamorph.getAttribute().st_ctime)
	
	finalList=[]
	for i in range(0,len(musicList)):
		finalList.append("".join(["\"",musicList[i].getObject(),"\""]))
	
	
	return finalList
	

	
if __name__ == "__main__":
	
	print "version: ", verNum
	switches=switchBoard(argv)
	musicList=loadMusic()
	
	if(len(musicList)>0):
		musicList.reverse()
		
		startScreening(musicList)
		
	else:
		print "No music to be screened available"
	
	
	