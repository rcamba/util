import unittest
import os

from string import rstrip
from tag import addTag, validateFilenameList, getFilenameList, getTagList

def clearFileContents(file):
	w=open(file,'w')#clear test log file
	w.close()

class testValidateFilenameList(unittest.TestCase):
	
	def setUp(self):
		print "\nStarting ", self._testMethodName,
	
	def testValidateStrOnly(self):
		filenameList=r"C:\Users\Kevin\Util\resources\unitTests\testTagFilesDir\d3.jpg"
		validFileList=validateFilenameList(filenameList)
		
		self.assertEqual(validFileList, 
		[r"C:\Users\Kevin\Util\resources\unitTests\testTagFilesDir\d3.jpg"] )
		
	def testValidateFileList(self):
		filenameList=[r"C:\Users\Kevin\Util\resources\unitTests\testTagFilesDir\d3.jpg", r"C:\Users\Kevin\Util\resources\unitTests\testTagFilesDir\d2.mp3", r"C:\Users\Kevin\Util\resources\unitTests\testTagFilesDir\d1.txt"]
		
		validFileList=validateFilenameList(filenameList)
		
		self.assertEqual(validFileList, filenameList)
		
	def testInvalidFileInList(self):
		filenameList=[r"C:\Users\Kevin\Util\resources\unitTests\testTagFilesDir\d3.jpg", r"C:\Users\Kevin\Util\resources\unitTests\testTagFilesDir\d2.mp3",
		r"C:\Users\Kevin\Util\resources\unitTests\testTagFilesDir\fakeFile1.txt"]
		
		validFileList=validateFilenameList(filenameList)
		
		self.assertEqual(validFileList, filenameList[:-1])
		
	def testInvalidStrInLList(self):
		filenameList=r"C:\Users\Kevin\Util\resources\unitTests\testTagFilesDir\fakeFile2.txt"
		
		validFileList=validateFilenameList(filenameList)
		self.assertEqual(validFileList, [])
	
	def testNoAbsPath(self):
		filenameList=r"d2.mp3"
		os.chdir(r"C:\Users\Kevin\Util\resources\unitTests\testTagFilesDir")
		validFileList=validateFilenameList(filenameList)
		
		
		resultList=[r"C:\Users\Kevin\Util\resources\unitTests\testTagFilesDir\d2.mp3"]
		
		self.assertEquals(validFileList,resultList)
		
	
class testAddAndGetTags(unittest.TestCase):
	def setUp(self):
		print "\nStarting ", self._testMethodName,
	
	
	def testCreatingTags(self):
		tagFile=r"C:\Users\Kevin\Util\resources\unitTests\tagFileTest.txt"

		clearFileContents(tagFile)

		addTag("testTag",[r"C:\Users\Kevin\Util\resources\unitTests\testTagFilesDir\d3.jpg"])
		
	
	
	def testGetFileList(self):
		tagFile=r"C:\Users\Kevin\Util\resources\unitTests\tagFileTest.txt"
		clearFileContents(tagFile)
		tList=[r"C:\Users\Kevin\Util\resources\unitTests\testTagFilesDir\d3.jpg"]
		addTag("testTag",tList)
		
		filenameList=getFilenameList("testTag")
		
		self.assertEqual(filenameList, tList)
		
	def testMultiGetFileList(self):
		tagFile=r"C:\Users\Kevin\Util\resources\unitTests\tagFileTest.txt"
		clearFileContents(tagFile)
		tList=[r"C:\Users\Kevin\Util\resources\unitTests\testTagFilesDir\d3.jpg",r"C:\Users\Kevin\Util\resources\unitTests\testTagFilesDir\d2.mp3"]
		addTag("testTag",tList)
	
		filenameList=getFilenameList("testTag")
		
		self.assertEqual(filenameList, tList)
		
	def testMultiTagMultiFile(self):
		tagFile=r"C:\Users\Kevin\Util\resources\unitTests\tagFileTest.txt"
		clearFileContents(tagFile)
		
		tList1=[r"C:\Users\Kevin\Util\resources\unitTests\testTagFilesDir\d3.jpg",r"C:\Users\Kevin\Util\resources\unitTests\testTagFilesDir\d2.mp3"]
		
		tList2=[r"C:\Users\Kevin\Util\resources\unitTests\testTagFilesDir\d1.txt"]
		
		addTag("testOrange",tList1)
		addTag("testRed",tList2)
	
		filenameList=getFilenameList("testOrange")
		self.assertEqual(filenameList, tList1)	
		
		filenameList=getFilenameList("testRed")
		self.assertEqual(filenameList, tList2)	
		
	def testUpdateTagFileList(self):
		tagFile=r"C:\Users\Kevin\Util\resources\unitTests\tagFileTest.txt"
		clearFileContents(tagFile)
		f1=r"C:\Users\Kevin\Util\resources\unitTests\testTagFilesDir\d3.jpg"
		f2=r"C:\Users\Kevin\Util\resources\unitTests\testTagFilesDir\d2.mp3"
		f3=r"C:\Users\Kevin\Util\resources\unitTests\testTagFilesDir\F9.txt"
		
		addTag("testRed",f1)
		addTag("testRed",f2)
		addTag("testRed",f3)
		addTag("testBlue",f3)
		
		
		filenameList=getFilenameList("testRed")
		self.assertEqual(filenameList,[f1,f2] )
		
		filenameList=getFilenameList("testBlue")
		self.assertEqual(filenameList,[])
		
	def testAddingDuplicates(self):
		tagFile=r"C:\Users\Kevin\Util\resources\unitTests\tagFileTest.txt"
		clearFileContents(tagFile)
		f1=r"C:\Users\Kevin\Util\resources\unitTests\testTagFilesDir\d3.jpg"
		f2=r"C:\Users\Kevin\Util\resources\unitTests\testTagFilesDir\d2.mp3"
		f3=r"C:\Users\Kevin\Util\resources\unitTests\testTagFilesDir\F9.txt"
		
		
		addTag("testGreen",[f1,f2,f3])
		addTag("testGreen",[f1,f2,f3])
		filenameList=getFilenameList("testGreen")
		self.assertEqual(filenameList,[f1,f2])
		
	def testFilenamesForTag(self):
		tagFile=r"C:\Users\Kevin\Util\resources\unitTests\tagFileTest.txt"
		clearFileContents(tagFile)
		f1=r"C:\Users\Kevin\Util\resources\unitTests\testTagFilesDir\d3.jpg"
		f2=r"C:\Users\Kevin\Util\resources\unitTests\testTagFilesDir\d2.mp3"
		
		addTag("testGreen",f1)
		addTag("testRed",[f1,f2])
		
		tagList=getTagList(f1)
		self.assertEqual( tagList, ["testGreen","testRed"])
		
		tagList=getTagList(f2)
		self.assertEqual( tagList, ["testRed"])
	
	def testTagsWithSpaces(self):
	
		tagFile=r"C:\Users\Kevin\Util\resources\unitTests\tagFileTest.txt"
		clearFileContents(tagFile)
		f1=r"C:\Users\Kevin\Util\resources\unitTests\testTagFilesDir\d3.jpg"
		f2=r"C:\Users\Kevin\Util\resources\unitTests\testTagFilesDir\d2.mp3"
		
		addTag("multi space tag",f1)
		addTag("multi space tag",f2)
		addTag("space1 space2 space3 space 4",f2)
		
		filenameList=getFilenameList("multi space tag")
		self.assertEqual(filenameList,[f1,f2])
		
		filenameList=getFilenameList("space1 space2 space3 space 4")
		self.assertEqual(filenameList,[f2])
	
	
	def testFileListFromMultiTags(self):
		tagFile=r"C:\Users\Kevin\Util\resources\unitTests\tagFileTest.txt"
		clearFileContents(tagFile)
		f1=r"C:\Users\Kevin\Util\resources\unitTests\testTagFilesDir\d3.jpg"
		f2=r"C:\Users\Kevin\Util\resources\unitTests\testTagFilesDir\d2.mp3"
		f3=r"C:\Users\Kevin\Util\resources\unitTests\testTagFilesDir\d1.txt"
		
		addTag("hatsune",f1)
		addTag("hatsune",f2)
		addTag("hatsune",f3)
		addTag("cover",f2)
		addTag("cover",f1)
		
		addTag("mull",f1)
		addTag("mull",f2)
		addTag("mull",f3)
		
		addTag("dd",f1)
		addTag("dd",f2)
		addTag("dd",f3)
		
		filenameList=getFilenameList(["hatsune", "cover"])
		self.assertEqual(filenameList,[f1,f2])
		
if __name__=="__main__":
	unittest.main()
	