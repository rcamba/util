#animedia player
#
#-a [folder location]
	#creates txt file marking last episode finished
	#plays next episode
#no args, display list of shows
	#select num
	#play next episode
	#mark curr episode as played
	
from root import switchBoard, printNumberedList, chooseFromNumberedList, animedLog
from sys import argv
from os import listdir, system, path
from string import replace

AVAILABLE_SWITCHES= ['a']

def addToMainAnimeDir(newDir):
	f=open(animedLog,"a")
	f.write(newDir)
	f.write("\n")
	f.close()

def playNextEp(anChoice):
	f=open(anChoice+"\\"+"[z]ampInfo.txt",'r')
	vidFile="\""+f.readline().replace("\n","")+"\""
	system( "\""+ vidFile +"\"")
	f.close()
	
	return vidFile
	
	
	
def loadNextEp(anChoice, lastEpisode):
	f=open(anChoice+"\\"+"[z]ampInfo.txt",'r')
	vidFileList=f.readlines()
	
	for i in range(0,len(vidFileList)):
		vidFileList[i]=vidFileList[i].replace("\n","")
		
	vidFileList.pop(0)
	
	
	writeToAmpInfo(anChoice, vidFileList, True)
	
	f.close()
	
def writeToAmpInfo(folder, fList=[], ignoreFolder=False):
	f=open(folder+"\\"+"[z]ampInfo.txt",'w')
	if( len(fList)==0 ):
		fList=listdir(folder)
	
	fList.sort()
	for file in fList:
		if "ampInfo" not in file:
		
			if(ignoreFolder==False):
				f.write(folder+"\\"+file.replace("\n",""))
			else:
				f.write(file.replace("\n",""))
			f.write("\n")
	f.close()


if __name__ == "__main__":
	switches=switchBoard(argv)
	
	if 'a' in switches:
		
		
		writeToAmpInfo(argv[1])
		addToMainAnimeDir(argv[1])
		
	else:
		f=open(animedLog,"r")
		animeList=f.readlines()
		
		for i in range(0,len(animeList)):
			animeList[i]=animeList[i].replace("\n","")
			

		printNumberedList(animeList)
		choice=chooseFromNumberedList(animeList)
		
		lastEpisode=playNextEp(animeList[choice])
		loadNextEp(animeList[choice],lastEpisode)
		
		
		
		
		
		