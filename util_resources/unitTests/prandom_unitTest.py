
import unittest
import inspect
from string import rstrip, lower


from prandom import VALID_EXTENSIONS, prune_song_list, get_song_list, SongLogHandler, SongLog

def clearTestSongLog(songsLogFile):
	w=open(songsLogFile,'w')#clear test log file
	w.close()

class Test_GetSongList(unittest.TestCase):
	def setUp(self):
		print "\nStarting ", self._testMethodName,


	def testFullPath(self):
		songDirectory=r"C:\Users\Kevin\Util\resources\unitTests\testSongDirectory"
		songList=get_song_list(songDirectory)
		self.assertEqual (songList,
		[r"c:\users\kevin\util\resources\unittests\testsongdirectory\songfile1.mp3",r"c:\users\kevin\util\resources\unittests\testsongdirectory\songfile2.m4a",	r"c:\users\kevin\util\resources\unittests\testsongdirectory\songfile3.flac"] )

	def testMaxNumber(self):
		songDirectory=r"C:\Users\Kevin\Util\resources\unitTests\testSongDirectory"

		songList=get_song_list(songDirectory)
		self.assertEqual(len(songList), 3)


	def testPrune(self):

		songList=[r"C:\textfile.txt",r"C:\songFile1.mp3",r"C:\NoExt", r"C:\vidFile.mp4",r"C:\songFile2.flac"]

		self.assertEqual(prune_song_list(songList), [r"C:\songFile1.mp3", r"C:\songFile2.flac"])

class Test_SongLogClasses(unittest.TestCase):
	def setUp(self):
		print "\nStarting ", self._testMethodName,


	def testLogSongs(self):
		songDirectory=r"C:\Users\Kevin\Util\resources\unitTests\testSongDirectory"
		songsLogFile=r"C:\Users\Kevin\Util\resources\unitTests\TestPrandomSongsLog.log"

		clearTestSongLog(songsLogFile)

		songList=get_song_list(songDirectory)

		slh=SongLogHandler(songsLogFile)

		slh.log_songs(songList)

		resultList=[r"c:\users\kevin\util\resources\unittests\testsongdirectory\songfile1.mp3=1",r"c:\users\kevin\util\resources\unittests\testsongdirectory\songfile2.m4a=1",	r"c:\users\kevin\util\resources\unittests\testsongdirectory\songfile3.flac=1"]

		slh.reload()
		songLogList= slh.song_log_list
		self.assertEqual( resultList, map(str,songLogList) )

		slh.log_songs(songList)
		resultList=[r"c:\users\kevin\util\resources\unittests\testsongdirectory\songfile1.mp3=2",r"c:\users\kevin\util\resources\unittests\testsongdirectory\songfile2.m4a=2",	r"c:\users\kevin\util\resources\unittests\testsongdirectory\songfile3.flac=2"]

		slh.reload()
		songLogList= slh.song_log_list
		self.assertEqual( resultList, map(str,songLogList) )






	def testInitSongHandler(self):
		songDirectory=r"C:\Users\Kevin\Util\resources\unitTests\testSongDirectory"
		songsLogFile=r"C:\Users\Kevin\Util\resources\unitTests\TestPrandomSongsLog.log"

		clearTestSongLog(songsLogFile)

		slh=SongLogHandler(songsLogFile)
		songLogList= slh.song_log_list
		self.assertEqual(len(songLogList),0)

		songList=get_song_list(songDirectory)
		slh.log_songs(songList)
		self.assertEqual(len(songLogList),3)

		filenameList=[]
		playCountList=[]
		for songLog in songLogList:
			filenameList.append(songLog.filename)
			playCountList.append(songLog.playCount)
		self.assertEqual( filenameList,[r"c:\users\kevin\util\resources\unittests\testsongdirectory\songfile1.mp3",r"c:\users\kevin\util\resources\unittests\testsongdirectory\songfile2.m4a",	r"c:\users\kevin\util\resources\unittests\testsongdirectory\songfile3.flac"])

		self.assertEqual(playCountList, [1,1,1])

		for songLog in songLogList:
			filenameList.append(songLog.filename)

	def testSongLogClass(self):

		sLog1=SongLog(r"C:\Users\Kevin\Util\resources\unitTests\testSongDirectory\songFile1.mp3",1)

		sLog2=SongLog(r"C:\Users\Kevin\Util\resources\unitTests\testSongDirectory\songFile2.mp3",2)

		self.assertEqual( sLog1.playCount, 1)

		self.assertEqual( str(sLog1), r"C:\Users\Kevin\Util\resources\unitTests\testSongDirectory\songFile1.mp3=1")

		self.assertEqual( sLog2+2, r"C:\Users\Kevin\Util\resources\unitTests\testSongDirectory\songFile2.mp3=4")




if __name__=="__main__":
	unittest.main()