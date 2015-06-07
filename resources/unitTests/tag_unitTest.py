import unittest


from string import rstrip, lower
import tag
from mock import MagicMock, patch, mock_open
from os import chdir, listdir

class MockOpen(object):
	def __init__(self,resultList):
		self.resultList=resultList

	def __call__(self,*args,**kwargs):
		return self

	def read(self,*args):
		return self.resultList.pop(0)


class TestValidateFilenameList(unittest.TestCase):

	def setUp(self):
		print "\nStarting ", self._testMethodName,

	def testValidateStrOnly(self):
		filenameList=f1
		validFileList=tag.validateFilenameList(filenameList)

		self.assertEqual(validFileList,
		[f1] )

	def testValidateFileList(self):
		filenameList=[f1,f2,f3]

		validFileList=tag.validateFilenameList(filenameList)

		self.assertEqual(validFileList, filenameList)

	def testInvalidFileInList(self):
		filenameList=[f1,f2, invf1]

		validFileList=tag.validateFilenameList(filenameList)

		self.assertEqual(validFileList, filenameList[:-1])

	def testInvalidStrInLList(self):
		filenameList=invf1

		validFileList=tag.validateFilenameList(filenameList)
		self.assertEqual(validFileList, [])

	def testNoAbsPath(self):
		filenameList=r"d2.mp3"
		chdir(r"c:\users\kevin\util\resources\unittests\testtagfilesdir")
		validFileList=tag.validateFilenameList(filenameList)

		resultList=[f2]

		self.assertEquals(validFileList,resultList)

	def testValidateFilename(self):
		res=tag.validateFilename(f1)
		self.assertEqual(res, f1)

		res=tag.validateFilename(invf1)
		self.assertEqual(res, "")


class TestAddAndGetTags(unittest.TestCase):
	def setUp(self):
		print "\nStarting ", self._testMethodName, "\n"


	def testAddingTags(self):
		mo=MockOpen(["testtag::"+f2])
		tag.open=mo
		tag.listdir=lambda x: ["testtag"]
		tag.__writeTagFile__= MagicMock()

		tag.addTags(["testTag"],f1)
		tag.__writeTagFile__.assert_called_with({"testtag":[f1]},'a')


	def testTagsWithSpaces(self):
		res="multi space tag::"+f1+" "+f2
		mo=MockOpen([res,res])
		tag.open=mo
		tag.listdir=lambda x: ["multi space tag"]
		tag.__writeTagFile__= MagicMock()

		tag.addTags(["multi space tag"],f1)
		tag.__writeTagFile__.assert_called_with({"multi space tag":[f1]},'a')

		tag.addTags(["multi space tag"],f2)
		tag.__writeTagFile__.assert_called_with({"multi space tag":[f2]},'a')


	def testMultiTagsOnFile(self):
		mo=MockOpen(["spaceship::"+"\""+f1+"\""])
		tag.open=mo
		tag.listdir=lambda x: ["spaceship"]
		tag.__writeTagFile__= MagicMock()

		tag.addTags(["hats", "blue square", "spaceship"],f2)

		tag.__writeTagFile__.assert_called_with({
		"hats":[f2],
		"blue square":[f2],
		"spaceship":[f2]},
		'a')


	def testAddingDuplicates(self):
		res="testgreen::"+"\""+f1+"\""+" "+"\""+f2+"\""
		mo=MockOpen([res,res])
		tag.open=mo
		tag.listdir=lambda x: ["testgreen"]
		tag.__writeTagFile__= MagicMock()

		tag.addTags(["testGreen"],f1)
		tag.addTags(["testGreen"],f2)

		tag.__writeTagFile__.assert_called_with({},'a')


	def testTaggingInvalidFile(self):
		res="testgreen::"+"\""+f1+"\""
		mo=MockOpen([res])
		tag.open=mo
		tag.logRemovedFile=lambda x: None
		tag.listdir=lambda x: ["testgreen"]
		tag.__writeTagFile__= MagicMock()

		tag.addTags(["testGreen"],invf1)
		tag.addTags(["testRed", "testBlue"],invf1)

		tag.__writeTagFile__.assert_called_with({},'a')


	def testGetFileList(self):
		rtdHolder=tag.reconstructTagDict
		res={
			"testtag": [f1],
		}

		tag.reconstructTagDict=MagicMock(side_effect=[res])

		filenameList=tag.getFilenameList("testTag")
		self.assertEqual(filenameList, res["testtag"])

		tag.reconstructTagDict=rtdHolder


	def testMultiGetFileList(self):
		rtdHolder=tag.reconstructTagDict
		res={
			"orange": [f2,f3]
		}

		tag.reconstructTagDict=MagicMock(side_effect=[res])

		filenameList=tag.getFilenameList("oRanGe")
		self.assertEqual(filenameList, res["orange"])

		tag.reconstructTagDict=rtdHolder


	def testGetMixedFilenameList(self):
		rtdHolder=tag.reconstructTagDict
		res={
			"diamond": [f1],
			"purple": [f1,f2]
		}

		tag.reconstructTagDict=MagicMock(side_effect=[res,res])

		res=tag.getMixedFilenameList(["diamond","purple"])
		self.assertEqual( len(res), 2)
		self.assertEqual( set(res),  set( [f1,f2]) )

		tag.reconstructTagDict=rtdHolder

	def testGetTagList(self):
		rtdHolder=tag.reconstructTagDict
		res={
			"testgreen": [f1],
			"testred": [f1,f2]
		}

		tag.reconstructTagDict=MagicMock(side_effect=[res,res])

		tagList=tag.getTagList(f1)
		self.assertEqual( tagList, ["testgreen","testred"])

		tagList=tag.getTagList(f2)
		self.assertEqual( tagList, ["testred"])

		tag.reconstructTagDict=rtdHolder


	def testRemoveTags(self):
		res1="testgreen::"+"\""+f1+"\""
		res2="testred::"+"\""+f1+"\""+" " +"\""+f2+"\""
		mo=MockOpen([res1,res2])
		tag.open=mo
		tag.logRemovedFile=lambda x: None
		tag.listdir=lambda x: ["testred","testgreen"]
		tag.__writeTagFile__= MagicMock()


		tag.removeTags(["testgreen"], f1)
		tag.__writeTagFile__.assert_called_with({"testgreen":[]},'w')

		tag.removeTags(["testred"], f1)
		tag.__writeTagFile__.assert_called_with({"testred":[f2]},'w')


	def testTagMultipleFiles(self):
		res="abc::"+"\""+f1+"\""
		mo=MockOpen([res,res,res])
		tag.open=mo
		tag.listdir=lambda x: ["abc"]
		tag.__writeTagFile__= MagicMock()

		fList=[f1,f2,f3]
		tag.tagMultipleFiles("test multi tag", fList)
		tag.__writeTagFile__.assert_any_call({"test multi tag":[f1]},'a')
		tag.__writeTagFile__.assert_any_call({"test multi tag":[f2]},'a')
		tag.__writeTagFile__.assert_any_call({"test multi tag":[f3]},'a')

		tag.tagMultipleFiles("abc",  fList)
		tag.__writeTagFile__.assert_any_call({"abc":[f2]},'a')
		tag.__writeTagFile__.assert_any_call({"abc":[f3]},'a')



def getAddAndGetTags_TS():

	addAndGetTags_suite= unittest.TestSuite()
	addAndGetTags_suite.addTest( TestAddAndGetTags("testAddingTags") )
	addAndGetTags_suite.addTest( TestAddAndGetTags("testTagsWithSpaces") )
	addAndGetTags_suite.addTest( TestAddAndGetTags("testMultiTagsOnFile") )
	addAndGetTags_suite.addTest( TestAddAndGetTags("testAddingDuplicates") )
	addAndGetTags_suite.addTest( TestAddAndGetTags("testTaggingInvalidFile") )

	addAndGetTags_suite.addTest( TestAddAndGetTags("testGetFileList") )
	addAndGetTags_suite.addTest( TestAddAndGetTags("testMultiGetFileList") )
	addAndGetTags_suite.addTest( TestAddAndGetTags("testGetMixedFilenameList") )

	addAndGetTags_suite.addTest( TestAddAndGetTags("testGetTagList") )

	addAndGetTags_suite.addTest( TestAddAndGetTags("testRemoveTags") )

	addAndGetTags_suite.addTest( TestAddAndGetTags("testTagMultipleFiles") )

	return addAndGetTags_suite

def getValidateFList_TS():

	validateFList_suite= unittest.TestSuite()
	validateFList_suite.addTest( TestValidateFilenameList("testValidateStrOnly") )
	validateFList_suite.addTest( TestValidateFilenameList("testValidateFileList") )
	validateFList_suite.addTest( TestValidateFilenameList("testInvalidFileInList") )
	validateFList_suite.addTest( TestValidateFilenameList("testInvalidStrInLList") )
	validateFList_suite.addTest( TestValidateFilenameList("testNoAbsPath") )
	validateFList_suite.addTest( TestValidateFilenameList("testValidateFilename") )

	return validateFList_suite


if __name__=="__main__":
	testTagFile=r"c:\users\kevin\util\resources\unittests\tagfiletest.log"
	testLogsDir=r"c:\users\kevin\util\resources\unittests\tagLogsTest"


	f1=r"c:\users\kevin\util\resources\unittests\testtagfilesdir\d1.txt"
	f2=r"c:\users\kevin\util\resources\unittests\testtagfilesdir\d2.mp3"
	f3=r"c:\users\kevin\util\resources\unittests\testtagfilesdir\d3.jpg"

	invf1=r"c:\users\kevin\util\resources\unittests\testtagfilesdir\fake9.txt"

	suiteList=[]

	addAndGetTags_suite=getAddAndGetTags_TS()
	validateFList_suite=getValidateFList_TS()

	suiteList.append(validateFList_suite)
	suiteList.append(addAndGetTags_suite)
	fullSuite = unittest.TestSuite(suiteList)
	runner = unittest.TextTestRunner()
	runner.run(fullSuite)
