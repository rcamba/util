import unittest

from root import switchParser

class TestSwitchParser(unittest.TestCase):
	
	def setUp(self):
		print "\nStarting ", self._testMethodName,
		
	def testValidSwitch(self):
		AVAILABLE_SWITCHES=['p']
		argv=["program.py","-p"]
		switchDict=switchParser(argv, AVAILABLE_SWITCHES)
		
		self.assertTrue( switchDict.has_key('p') )
	
	def testMultiValidSwitches(self):
		AVAILABLE_SWITCHES=['p','s']
		argv=["program.py","-p","-s"]
		
		switchDict=switchParser(argv,AVAILABLE_SWITCHES)
		
		self.assertTrue(switchDict.has_key('p'))
		self.assertTrue(switchDict.has_key('s'))
	
	
	def testInvalidSwitch(self):
		
		AVAILABLE_SWITCHES=['p']
		argv=["program.py","-z"]
		
		with self.assertRaises(SystemExit) as cm:
			switchDict=switchParser(argv,AVAILABLE_SWITCHES)
		self.assertEqual(cm.exception.code, 1)
		
	def testValidSwitchPosition(self):
		AVAILABLE_SWITCHES=['p','#','s','z']
		argv=["program.py","tagName", "-z","stuff","-#:30","moreStuff","-p"]
		switchDict=switchParser(argv,AVAILABLE_SWITCHES)
		
		self.assertTrue(switchDict.has_key('z'))
		self.assertTrue(switchDict.has_key('#'))
		self.assertTrue(switchDict.has_key('p'))
		self.assertTrue("tagName" in argv)
		self.assertTrue("stuff" in argv)
		self.assertTrue("moreStuff" in argv)
		
	def testMultiWordInSwitch(self):
		AVAILABLE_SWITCHES=['p','f','e','z']
		argv=["program.py","tagName", "-e:orange monkey eagle","stuff","-f:files with spaces"]
		switchDict=switchParser(argv,AVAILABLE_SWITCHES)
		
		self.assertEqual(switchDict['e'], "orange monkey eagle")
		self.assertEqual(switchDict['f'], "files with spaces")
		self.assertTrue("tagName" in argv)
		self.assertTrue("stuff" in argv)
		
	def testCommaInSwitch(self):
		AVAILABLE_SWITCHES=['p','f','e','z']
		argv=["program.py","tagName", "-e:sad, instrumental","-f:files ,with ,commas"]
		switchDict=switchParser(argv,AVAILABLE_SWITCHES)
		self.assertEqual(switchDict['f'],"files ,with ,commas")
		self.assertEqual(switchDict['e'],"sad, instrumental")
		
if __name__=="__main__":
	unittest.main()