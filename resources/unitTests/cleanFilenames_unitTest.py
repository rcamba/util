import unittest
import os

from cleanFilenames import cleanString, cleanChars

class TestCleanString(unittest.TestCase):
	def setUp(self):
		print "\nStarting ", self._testMethodName,
	
	def test_invalid_emptyResult(self):
		dirty="!@$%;: _'#.-()"
		correct="pass.test"
		outMsg=[]
		cleaned=cleanString(dirty,outMsg)
		self.assertTrue("Error: Cleaned filename is empty because it only consisted of non-alphanumeric characters." in outMsg)
		self.assertEqual(cleaned, correct)
		
		
class TestCleanChars(unittest.TestCase):
	
	def setUp(self):
		print "\nStarting ", self._testMethodName,
		
	def test_invalidChars(self):
		dirty="fname !@$%;: _'#.-()"
		correct="fname _'#.-()"
		cleaned=cleanChars(dirty)
		self.assertEqual(cleaned, correct)
		
	def test_multipleSpaces(self):
		dirty=" a_b   c_d  e_f g_h    "
		correct="a_b c_d e_f g_h"
		cleaned=cleanChars(dirty)
		self.assertEqual(cleaned, correct)
		
	def test_caps(self):
		dirty="SHOULDN'T CHANGE"
		correct="SHOULDN'T CHANGE"
		cleaned=cleanChars(dirty)
		self.assertEqual(cleaned, correct)
	
	def test_invalidStartChar(self):
		dirty="_'_#nonAlphaNumStart"
		correct="nonAlphaNumStart"
		cleaned=cleanChars(dirty)
		self.assertEqual(cleaned, correct)
		
		dirty="[exception] start_with_["
		correct="[exception] start_with_["
		cleaned=cleanChars(dirty)
		self.assertEqual(cleaned, correct)
		
if __name__=="__main__":
	
	suiteList=[]
	
	cleanChars_ts=unittest.TestSuite()
	cleanChars_ts.addTest( TestCleanChars("test_invalidChars") )
	cleanChars_ts.addTest( TestCleanChars("test_multipleSpaces") )
	cleanChars_ts.addTest( TestCleanChars("test_caps") )
	cleanChars_ts.addTest( TestCleanChars("test_invalidStartChar") )
	
	cleanString_ts=unittest.TestSuite()
	cleanString_ts.addTest( TestCleanString("test_invalid_emptyResult") )
	
	suiteList.append(cleanChars_ts)
	suiteList.append(cleanString_ts)
	
	fullSuite = unittest.TestSuite(suiteList)
	runner = unittest.TextTestRunner()
	runner.run(fullSuite)
	