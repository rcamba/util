from os import system, listdir, path, stat
from sys import argv
from root import musicDir
from tag import getFilenameList


class AttributeContainer:
	pass


VALID_EXTENSIONS = ["mp3","m4a","flac","ogg","mka", "opus"]


def getSongList():

	if len(argv)>1:
		return getFilenameList(argv[1])
	else:
		return [path.join(musicDir,f) for f in listdir(musicDir)]


def playRecentSongs(sortedSongList):

	for song in sortedSongList:
		if path.splitext(song)[1][1:].lower() in VALID_EXTENSIONS:
			system("\"{}\"".format(
				path.normpath(song)))


if __name__ == "__main__":

	SONG_LIMIT = 10
	initSongList = getSongList()

	acList = []
	for song in initSongList:
		ac = AttributeContainer()
		ac.song = song
		ac.stat = stat(song)
		acList.append(ac)

	sortedAcList = sorted(acList,
		key=lambda AttributeContainer:AttributeContainer.stat.st_ctime,
		reverse=True)

	sortedSongList = [s.song for s in sortedAcList][:SONG_LIMIT]

	playRecentSongs(sortedSongList)
