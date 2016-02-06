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


def kill_VLC():

	vlc_killed = False
	for proc in process_iter():

		if proc.pid == glob_vlc_proc.pid:
			proc.kill()
			proc.wait()

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


def addToDeletedLog(targ):
	writer=open(deletedScreenedLog,'a')
	targ=targ.replace("\"","")
	targ=path.splitext(path.split(targ)[1])[0]
	writer.write(targ)
	writer.write("\n")
	writer.close()


def handleTagging(musicFileName):

	try:
		move(musicFileName, musicDir)
		removeTags(["screen"], musicFileName, validate=False)

		filename="".join([musicDir,"\\",cutDir(musicFileName)])
		tagList=raw_input("Enter tag(s). Separate with commas\n").split(',')
		print ""
		addTags(tagList,filename)

	except shutil_error, e:

		errorAlert("{m} already exists in music directory.\nDeleting {m}".format(
			m=musicFileName))
		handleDelete(musicFileName)


def handleDelete(musicFileName):

	try:

		os_remove(musicFileName)
		removeTags(["screen"], musicFileName, validate=False)
		print "Delete successful\n"
		addToDeletedLog(musicFileName)

	except OSError, e:
		errorAlert("Failed to delete file {}. No changes have been made.".format(
			musicFileName))
		print e.message
		raise


def handleKeep(musicFileName):

	try:
		move(musicFileName, musicDir)
		removeTags(["screen"], musicFileName, validate=False)
		print "Move successful\n"

	except shutil_error, e:

		errorAlert("{m} already exists in music directory.\nDeleting {m}".format(
			m=musicFileName))
		handleDelete(musicFileName)


def start_screening(song_list):

	global glob_vlc_proc

	class Quit:
		def __init__(self):
			self.quit = False
		def set_to_true(self):
			self.quit = True

	q = Quit()

	for song in song_list:

		invalid_key_press = 0

		if q.quit is False:

			playMusicCommand = ([MEDIA_PLAYER_PROGRAM] +
				MEDIA_PLAYER_OPTIONS + [song])

			glob_vlc_proc = Popen(playMusicCommand)

			print "Playing: ", song

			prompt = getKeyPress()

			while prompt not in ['k', 'd', 't', 'q']:
				print "Invalid selection"
				invalid_key_press += 1
				if invalid_key_press > 2:
					confirm_resume = False
					errorAlert("Too many invalid keypresses->Pausing")

					while(confirm_resume is False):
						confirm_resume = getResumeConfirmation()

				prompt = getKeyPress()

			else:
				kill_VLC()

				char_func_mapping = {
					'k': lambda: handleKeep(song),
					'd': lambda: handleDelete(song),
					't': lambda: handleTagging(song),
					'q': q.set_to_true
				}

				char_func_mapping[prompt]()
				song_list.remove(song)


def get_songs():

	song_list = getFilenameList(["screen"])
	shuffle(song_list)
	return song_list


if __name__ == "__main__":

	MEDIA_PLAYER_PROGRAM = "C:\\Program Files (x86)\\VideoLAN\\VLC\\vlc.exe"

	MEDIA_PLAYER_OPTIONS = "--qt-start-minimized --one-instance --playlist-enqueue --playlist-autostart --no-crashdump -L".split()

	glob_vlc_proc = None

	song_list = get_songs()

	if len(song_list) > 0:
		start_screening(song_list)

	else:
		errorAlert("No music to be screened available")