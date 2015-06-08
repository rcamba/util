"""

Plays the x most recent songs
-x can be a negative or positive integer
-negative values indicate play from oldest songs
-default value for x is 10

"""
from os import system, listdir, path
from sys import argv
from root import musicDir, switchParser
from getNewestFile import sortByCreationTime
from tag import getFilenameList

AVAILABLE_SWITCHES=['t','#']
VALID_EXTENSIONS=["mp3","m4a","flac","ogg","mka"]

def loadSongs():
	if 't' in switches:
		return getFilenameList(switches['t'])
	else:
		return [path.join(musicDir,f) for f in listdir(musicDir)]

def getMaxNum():
	if '#' in switches:
		return switches['#']
	else:
		return 10

def playRecentSongs(sortedSongList):

	for song in sortedSongList:
		if path.splitext(song)[1][1:].lower() in VALID_EXTENSIONS:
			system(song)

if __name__ == "__main__":
	switches=switchParser(argv, AVAILABLE_SWITCHES)

	songList=loadSongs()
	maxNum=getMaxNum()
	sortedSongList=sortByCreationTime(songList)
	sortedSongList=sortedSongList[:maxNum]
	playRecentSongs(sortedSongList)



