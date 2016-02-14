from os import listdir, path, getcwd
from string import rstrip, strip, lower
from random import randint
from operator import attrgetter
from sys import argv, stdin
from threading import Thread

from root import musicDir, switchParser, songLogFile, pipedList, errorAlert, prandomExceptions
from tag import getFilenameList, getMixedFilenameList
from subprocess import Popen

VALID_EXTENSIONS=["mp3", "m4a", "flac", "ogg", "mka", "opus"]
AVAILABLE_SWITCHES=['#','e','m']

class SongLogHandler:
	def __init__(self,songsLogFile):
		self.songsLogFile=songsLogFile
		self.loadLog(songsLogFile)

	def logSongs(self,songList):
		songList=map(lower,songList)
		for song in songList:
			for songLog in self.songLogList[:]:#iterate through a copy
				if(song==songLog.filename):
					songLog.playCount=int(songLog.playCount)+1
					break
			else:#song not found in songLogList i.e first time played
				newSongLog=SongLog(song,1)
				self.songLogList.append(newSongLog)

		self.songLogList.sort(key=attrgetter("playCount") , reverse=True)

		writer=open(self.songsLogFile,'w')
		for songLog in self.songLogList:
			writer.write(songLog+"\n")
		writer.close()

	def loadLog(self,songsLogFile):
		reader=open(songsLogFile)
		self.songLogList=map(rstrip,reader.readlines())
		for i in range(0,len(self.songLogList)):
			token=self.songLogList[i].split('=')
			self.songLogList[i]=SongLog(token[0],token[1])

	def reload(self):
		self.loadLog(self.songsLogFile)

class SongLog:
	def __init__(self,newFilename,newPlayCount):
		self.filename=newFilename
		self.playCount=int(newPlayCount)

	def __add__(self, other):
		if type(other)==int:
			self.playCount=self.playCount+other
			return self.__str__()
		else:
			return self.__str__() + str(other)

	def __str__(self):
		return self.filename+"="+str(self.playCount)

def pruneSongList(songList):
	for song in songList[:]: #Iterate through a copy to avoid skipping items or doing reverse iteration
		songExtension=path.splitext(song)[1][1:]
		if songExtension not in VALID_EXTENSIONS:
			songList.remove(song)

	return songList

def getSongList(musicDir):
	"""Return list of songs with full path"""

	def createFullPath(filename): #helper function for map function
		return lower(musicDir+"\\"+filename)

	songList=listdir(musicDir)

	songList=pruneSongList(songList)
	songList=map(createFullPath,songList)

	return songList


def getSongListFromTag(tagList, switches):
	tagList=map(strip, tagList)

	if 'm' in switches:
		print "Getting mixed tags: ", tagList
		songList=getMixedFilenameList(tagList)
	else:
		songList=getFilenameList(tagList)

	if len(songList)==0:
		errorAlert("No file list available for given tag(s)")


	return  songList

def pruneExceptions(songList, switches, default=True):

	if default:
		exec("exceptionList=" +open(prandomExceptions).read() )#... default exceptions
	else:
		exceptionList=[]

	exceptionSongList=[]

	if switches.has_key('e'):#exception, i.e don't play songs with this tag
		exceptionList.extend( switches['e'].split(',') )

	for exception in exceptionList:
		exceptionSongList.extend(getFilenameList( exception) )

	for exceptionSong in exceptionSongList:
		if exceptionSong in songList: #if tag is given, songList may not have exceptionSong - when no tag is given, all songs are in songList so exceptionSong will always be in it
			songList.remove(exceptionSong)


	return songList

def playSongs(songList):
	for song in songList:


		Popen([song], shell=True)


def randomSelect(songList,maxNum):
	finalSongList=[]

	for i in range(0,maxNum):
		sel= randint(0,len(songList)-1)
		finalSongList.append( songList[sel])
		songList.remove(songList[sel])

	return finalSongList

def getMaxNum(argv, switches,songList):
	if switches.has_key('#'):
		maxNum=int(switches['#'])

	elif len(argv)>1 and len(songList)<60:
		maxNum=len(songList)

	else:
		maxNum=60

	return maxNum

def handlePiping():

	songList=pipedList("".join(map(str,stdin.readlines())))


	i=0
	for file in songList[:]:#prune
		if (path.isabs(file)==False):
			songList[i]= getcwd()+"\\"+songList[i]
		#file=songList[i]
		ext=path.splitext(file)[1][1:]
		if ext not in VALID_EXTENSIONS:
			print ext, "not a valid extension. Removing", songList[i], " from list"
			songList.remove(file)
		i=i+1
	return songList

def main(argv):
	switches = switchParser(argv)
	if stdin.isatty() is False:#for using with nf/search
		prunedSongList=handlePiping()
		maxNum=len(prunedSongList)
		print "Playing " + str(maxNum) + " piped songs"
	else:

		if len(argv)>1:
			songList=getSongListFromTag(" ".join(map(str,argv[1:])).split(','), switches)
			prunedSongList=pruneExceptions(songList, switches, default=False)
		else:
			songList=getSongList(musicDir)
			prunedSongList=pruneExceptions(songList, switches)

		maxNum=getMaxNum(argv,switches,prunedSongList)

	finalSongList=randomSelect(prunedSongList,maxNum)

	slh=SongLogHandler(songLogFile)
	slh.logSongs(finalSongList)

	playSongs(finalSongList)

if __name__=="__main__":
	main(argv)
