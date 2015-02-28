"""

Downloads picture to certain folder 
Folder destination can be changed through parameters
Default destination if called without parameters: root.picDir

Usage:
directPicToFolder.py [opt args] [picture link]

Optional args:
[a]theism
[c]haud
[g]ifs
[r]age
[v]ertical
[w]ebcomics

"""
import os
import sys
import root

def getFolder(letter=""):
	
	if(len(letter)<1):
		folder=root.picDir
	
	elif(letter=="a"):
		folder=root.atheismDir
	
	elif(letter=="c"):
		folder=root.chaudDir
	
	elif(letter=="g"):
		folder=root.gifsDir
		
	elif(letter=="r"):
		folder=root.rageComicsDir
	
	elif(letter=="v"):
		folder=root.verticalDir
		
	elif(letter=="w"):
		folder=root.webComicsDir
		
	else:
		print "Invalid folder parameter"
		folder=""
		
	return folder
def downloadToFolder(folder, targetLink):
	
	
	if(folder!=""):
		command="".join(["wget -q -P",folder," ",targetLink])
		os.system(command)
		
		#s="".join(["nF ",folder])
		#os.system(s)
	
if __name__ == "__main__":
	
	if(len(sys.argv)>2):
		folder=getFolder( str(sys.argv[1]) )
		downloadToFolder(folder, str(sys.argv[2]) )
		
	elif(len(sys.argv)>1):
		folder=getFolder()
		downloadToFolder(folder, str(sys.argv[1]) )
	
	else:
		print "Missing parameters"
		sys.exit(1)