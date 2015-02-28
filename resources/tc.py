from root import keyboardType, getClipboardData
from sys import argv

if __name__ == "__main__":
	cData=getClipboardData()
	
	for arg in argv[1:]:
		keyboardType(arg)
		keyboardType(" ")
	
	for ch in cData:
		keyboardType(ch)
		
	