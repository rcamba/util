"""

Plays the x most recent songs
-x can be a negative or positive integer
-negative values indicate play from oldest songs
-default value for x is 10

"""
from os import system, listdir, stat
from sys import argv
from root import musicDir

def _loadSongs():
	songList=[]
	list=listdir(musicDir)
	for i in range(0, len(list)):
		
		fileName="".join([musicDir,"/",list[i]])
		fileStat= stat(fileName)
		
		songList.append([ (fileStat.st_ctime), ("".join([musicDir,"/\"",list[i],"\""])) ])
		
	songList.sort()
	
	return songList

def _playRecentSongs(numOfSongs=10):
	
	songList=_loadSongs()
	
	if(numOfSongs>0):
		start=(len(songList)-1)
		end=(len(songList)-1)-numOfSongs
		inc=-1
	else:
		start=0
		end=(numOfSongs*-1)
		inc=1
		
	for i in range(start, end, inc ):
		system(songList[i][1])

if __name__ == "__main__":
	
	if (len(argv)>1):
		if(int(argv[1])!=0):
			_playRecentSongs(int(argv[1]))
		else:
			print "Number of songs can't be 0"
	else:
		_playRecentSongs()
	
	