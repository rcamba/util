from tag import getFilenameList, addTags, removeTags
from root import screeningDir, musicDir, deletedScreenedLog, errorAlert
from os import listdir, kill, path, rename, getenv, pardir, remove as os_remove
from string import lower
from msvcrt import kbhit, getch

from psutil import process_iter
from shutil import move, Error as shutil_error
from sys import exit as sys_exit, argv
from random import shuffle
from subprocess import Popen


def killVLC():

	vlc_killed = False
	for proc in process_iter():

		if proc.pid == glob_vlc_proc.pid:
			proc.kill()
			vlc_killed = True
			break

	if not vlc_killed:
		raise Exception(
			"Failed to kill VLC process. PID: {} not found".format(
				glob_vlc_proc.pid))


def getKeyPress():

	print "Type [k] to keep, [t] to keep and tag, [d] to delete track or [q] for quit"
	result=""

	while (result==""):

		if kbhit():
			result = (getch())
			inputChar=ord(result)
			if(inputChar==224 or inputChar==0):
				getch()

	result=lower(result)
	return result

def getResumeConfirmation():
	print "Type 'continue' and press enter to resume"
	userIn=raw_input().lower()
	if userIn=="continue":
		return True
	else:
		print "You typed : " + userIn
		errorAlert("Type 'continue' and press enter to resume")
		return False

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

def addToDeletedLog(targ):
	writer=open(deletedScreenedLog,'a')
	targ=targ.replace("\"","")
	targ=path.splitext(path.split(targ)[1])[0]
	writer.write(targ)
	writer.write("\n")
	writer.close()

def handleDelete(musicList, i):

	removeTags(["screen"], musicList[i].replace("\"",""))
	os_remove( musicList[i].replace("\"","") )
	if path.exists(musicList[i])==False:
		print "Delete successful\n"
		addToDeletedLog(musicList[i])
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

	global glob_vlc_proc

	class Quit:
		def __init__(self):
			self.quit = False
		def set_to_true(self):
			self.quit = True

	q = Quit()
	for i in range(len(musicList)-1,-1,-1):
		invalidKeyPress=0
		if q.quit is False:

			playMusicCommand = [MEDIA_PLAYER_PROGRAM] + MEDIA_PLAYER_OPTIONS + [musicList[i]]

			glob_vlc_proc = Popen(playMusicCommand)

			print "Playing: ", musicList[i]

			prompt=getKeyPress()

			while all([prompt!="k", prompt!="d" , prompt!="t", prompt!="q"]):
				print "Invalid selection"
				invalidKeyPress+=1
				if invalidKeyPress>2:
					confirmResume=False

					errorAlert("Too many invalid keypresses->Pausing")
					while(confirmResume==False):

						confirmResume=getResumeConfirmation()

				prompt=getKeyPress()



			else:
				killVLC()

				musicFileName = musicList[i]

				charToFuncMapping = {
					'k': lambda: handleKeep(musicFileName, i),
					'd': lambda: handleDelete(musicList, i),
					't': lambda: handleTagging(musicList, musicFileName, i),
					'q': q.set_to_true
				}

				charToFuncMapping[prompt]()


def loadMusic():

	musicList = getFilenameList(["screen"])

	shuffle(musicList)

	finalList=[]
	for i in range(0,len(musicList)):
		finalList.append(musicList[i])

	return finalList


if __name__ == "__main__":

	MEDIA_PLAYER_PROGRAM = "C:\\Program Files (x86)\\VideoLAN\\VLC\\vlc.exe"

	MEDIA_PLAYER_OPTIONS = "--qt-start-minimized --one-instance --playlist-enqueue --playlist-autostart --no-crashdump -L".split()

	glob_vlc_proc = None

	musicList = loadMusic()

	if(len(musicList) > 0):
		startScreening(musicList)

	else:
		print "No music to be screened available"


