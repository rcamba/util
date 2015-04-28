import unittest
import os

from string import rstrip, lower
from tag import addTags, validateFilenameList, getFilenameList, getTagList, validateFilename, removeTags, tagMultipleFiles, getMixedFilenameList, setTagFile, loadTagDict


def clearFileContents(file):
	w=open(file,'w')#clear test log file
	w.close()

class TestValidateFilenameList(unittest.TestCase):
	
	def setUp(self):
		print "\nStarting ", self._testMethodName,
	
	def testValidateStrOnly(self):
		filenameList=f1
		validFileList=validateFilenameList(filenameList)
		
		self.assertEqual(validFileList, 
		[f1] )
		
	def testValidateFileList(self):
		filenameList=[f1,f2,f3]
		
		validFileList=validateFilenameList(filenameList)
		
		self.assertEqual(validFileList, filenameList)
		
	def testInvalidFileInList(self):
		filenameList=[f1,f2, invf1]
		
		validFileList=validateFilenameList(filenameList)
		
		self.assertEqual(validFileList, filenameList[:-1])
		
	def testInvalidStrInLList(self):
		filenameList=invf1
		
		validFileList=validateFilenameList(filenameList)
		self.assertEqual(validFileList, [])
	
	def testNoAbsPath(self):
		filenameList=r"d2.mp3"
		os.chdir(r"c:\users\kevin\util\resources\unittests\testtagfilesdir")
		validFileList=validateFilenameList(filenameList)
		
		
		resultList=[f2]
		
		self.assertEquals(validFileList,resultList)
	
	def testValidateFilename(self):
		res=validateFilename(f1)
		self.assertEqual(res, f1)
		
		res=validateFilename(invf1)
		self.assertEqual(res, "")
	
	
class TestAddAndGetTags(unittest.TestCase):
	def setUp(self):
		print "\nStarting ", self._testMethodName, "\n"
	
	def tearDown(self):
		clearFileContents(testTagFile)
	
	def testCreatingTags(self):
	
		
		addTags(["testTag"],f1)
		
	def testGetFileList(self):
		
		
		fList=[f1]
		for f in fList:
			addTags(["testTag"],f)
		
		filenameList=getFilenameList("testTag")
		
		self.assertEqual(filenameList, fList)
		
	def testMultiGetFileList(self):
		
		
		fList=[f1,f2]
		for f in fList:
			addTags(["testTag"],f)
	
		filenameList=getFilenameList("testTag")
		
		self.assertEqual(filenameList, fList)
		
	def testMultiTagMultiFile(self):
		
		
		
		fList1=[f1, f2]
		
		fList2=[f3]
		
		for f in fList1:
			addTags(["testOrange"],f)
		
		for f in fList2:
			addTags(["testRed"],f)
	
		filenameList=getFilenameList("testOrange")
		self.assertEqual(filenameList, fList1)	
		
		filenameList=getFilenameList("testRed")
		self.assertEqual(filenameList, fList2)	
		
	def testUpdateTagFileList(self):
		
		addTags(["testRed"],f1)		
		addTags(["testRed"],f2)
		addTags(["testRed", "testBlue"],invf1)
		
		filenameList=getFilenameList("testRed")
		self.assertEqual(filenameList,[f1,f2])
		
		filenameList=getFilenameList("testBlue")
		self.assertEqual(filenameList,[])
		
	def testAddingDuplicates(self):
		
		addTags(["testGreen"],f1)
		addTags(["testGreen"],f2)
		addTags(["testGreen"],invf1)
		
		addTags(["testGreen"],f1)
		addTags(["testGreen"],f2)
		addTags(["testGreen"],invf1)
		
		filenameList=getFilenameList("testGreen")
		self.assertEqual(filenameList,[f1,f2])
		
	def testFilenamesForTag(self):
		
		addTags(["testGreen"],f1)
		addTags(["testRed"],f1)
		addTags(["testRed"],f2)
		
		tagList=getTagList(f1)
		
		self.assertEqual( tagList, ["testgreen","testred"])
		
		tagList=getTagList(f2)
		self.assertEqual( tagList, ["testred"])
	
	def testTagsWithSpaces(self):
			
		addTags(["multi space tag"],f1)
		addTags(["multi space tag"],f2)
		addTags(["space1 space2 space3 space 4"],f2)
		
		filenameList=getFilenameList("multi space tag")
		self.assertEqual(filenameList,[f1,f2])
		
		filenameList=getFilenameList("space1 space2 space3 space 4")
		self.assertEqual(filenameList,[f2])
	
	
	def testFileListFromMultiTags(self):
		
		addTags(["hatsune", "cover", "ee"],f1)
		addTags(["hatsune", "cover","dd"],f2)
		addTags(["hatsune"],f3)
		
		filenameList=getFilenameList(["hatsune"])
		self.assertEqual(set(filenameList),set([f1,f2,f3]))
		
		filenameList=getFilenameList(["hatsune", "cover"])
		self.assertEqual( set(filenameList) , set([f1,f2]))
		
		filenameList=getFilenameList(["hatsune", "cover","ee"])
		self.assertEqual(set(filenameList),set([f1]))
		
	def testRemoveTags(self):
		
		initTags=["blue", "red","orange"]
		addTags(initTags,f1)
		
		tagList=getTagList(f1)
		self.assertEqual(set(initTags),set(tagList))
		
		removeTags(["blue"], f1)
		tagList=getTagList(f1)
		initTags.remove("blue")
		self.assertEqual(set(initTags), set(tagList))
		
		removeTags(["orange"], f1)
		tagList=getTagList(f1)
		initTags.remove("orange")
		self.assertEqual(set(initTags), set(tagList))
		
	def testTagMultipleFiles(self):
		initFList=[f1,f2,f3]
		tagMultipleFiles("test multi tag", initFList)
		
		filenameList=getFilenameList(["test multi tag"])
		self.assertEqual(initFList, filenameList)
		
		tagList=getTagList(f1)
		self.assertEqual(["test multi tag"], tagList)
		
		tagList=getTagList(f2)
		self.assertEqual(["test multi tag"], tagList)
		
		tagList=getTagList(f3)
		self.assertEqual(["test multi tag"], tagList)
	
	def testGetMixedFilenameList(self):
		addTags(["testRed",], f1)
		addTags(["testGreen"], f2)
		
		res=getMixedFilenameList(["testRed","testGreen"])
		self.assertEqual(set(res), {f1,f2})
		

		
		
		
		
if __name__=="__main__":
	testTagFile=r"c:\users\kevin\util\resources\unittests\tagfiletest.log"
	testLogsDir=r"c:\users\kevin\util\resources\unittests\tagLogsTest"
	
	setTagFile(testTagFile,testLogsDir)
	if len(loadTagDict()) !=0:
		print "TagDict not empty. Either not using proper file or file was not cleaned up properly after last run."
	
	else:
	
	
		
		f1=r"c:\users\kevin\util\resources\unittests\testtagfilesdir\d1.txt"
		f2=r"c:\users\kevin\util\resources\unittests\testtagfilesdir\d2.mp3"
		f3=r"c:\users\kevin\util\resources\unittests\testtagfilesdir\d3.jpg"
		
		invf1=r"c:\users\kevin\util\resources\unittests\testtagfilesdir\fake9.txt"
		
		suiteList=[]
		addAndGetTags_suite= unittest.TestSuite()
		addAndGetTags_suite.addTest( TestAddAndGetTags("testCreatingTags") )
		addAndGetTags_suite.addTest( TestAddAndGetTags("testGetFileList") )
		addAndGetTags_suite.addTest( TestAddAndGetTags("testMultiGetFileList") )
		addAndGetTags_suite.addTest( TestAddAndGetTags("testMultiTagMultiFile") )
		addAndGetTags_suite.addTest( TestAddAndGetTags("testUpdateTagFileList") )
		addAndGetTags_suite.addTest( TestAddAndGetTags("testAddingDuplicates") )
		addAndGetTags_suite.addTest( TestAddAndGetTags("testFilenamesForTag") )
		addAndGetTags_suite.addTest( TestAddAndGetTags("testTagsWithSpaces") )
		addAndGetTags_suite.addTest( TestAddAndGetTags("testFileListFromMultiTags") )
		addAndGetTags_suite.addTest( TestAddAndGetTags("testRemoveTags") )
		addAndGetTags_suite.addTest( TestAddAndGetTags("testTagMultipleFiles") )
		addAndGetTags_suite.addTest( TestAddAndGetTags("testGetMixedFilenameList") )
		
		
		validateFList_suite= unittest.TestSuite()
		validateFList_suite.addTest( TestValidateFilenameList("testValidateStrOnly") )
		validateFList_suite.addTest( TestValidateFilenameList("testValidateFileList") )
		validateFList_suite.addTest( TestValidateFilenameList("testInvalidFileInList") )
		validateFList_suite.addTest( TestValidateFilenameList("testInvalidStrInLList") )
		validateFList_suite.addTest( TestValidateFilenameList("testNoAbsPath") )
		validateFList_suite.addTest( TestValidateFilenameList("testValidateFilename") )
		
		suiteList.append(validateFList_suite)
		suiteList.append(addAndGetTags_suite)
		fullSuite = unittest.TestSuite(suiteList)
		runner = unittest.TextTestRunner()
		runner.run(fullSuite)
		