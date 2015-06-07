from time import sleep
from string import lower
from os import system, listdir, path
from threading import Thread
from bs4 import BeautifulSoup
from sys import argv
from cleanFilenames import cleanString

from root import screeningDir, musicDir, switchBoard, getAllPageLinks, ytDownloadsDir, ytAMVDir, outputFromCommand, errorAlert, deletedScreenedLog



"""
 -m single music
 -v multiple video
 -s single video
"""

MAX_TRIES=3
AVAILABLE_SWITCHES=['v','h','s','m']

YOUTUBE_DL="C:\\Users\\Kevin\\Util\\youtubeDL.py "

def getTitleFromSys(ytVidLink):

	YOUTUBE_DL="C:\\Users\\Kevin\\Util\\youtubeDL.py "
	commandArgs="".join([ytVidLink , " -q -s --get-filename --extract-audio --restrict-filenames --output %(title)s_%(id)s.%(ext)s "])
	title=outputFromCommand(YOUTUBE_DL+commandArgs)

	return title

def getVidList(linksList):
	vidList=[]
	for link in linksList:

		tempList=__getVidList( getAllPageLinks(link.replace('\\','/') ) )
		print "Retrieving video list from: ", link

		i=0
		while( len(tempList)==0 and i<MAX_TRIES):
			vidLinks=getAllPageLinks(link.replace('\\','/'))

			tempList=__getVidList(vidLinks)

			i=i+1
			print "Retry # ", i

			sleep(3)
		vidList.extend(tempList)

	return vidList

def __getVidList(vidLinks):

	vHashList=[]

	for i in range(len(vidLinks)-1,-1,-1):

		vidLinks[i]=vidLinks[i].get("href")
		if ( vidLinks[i] is not None):

			if "youtube" not in vidLinks[i]:
				vidLinks[i]="".join(["youtube.com",vidLinks[i]])

			if  "http" not in vidLinks[i] :
				vidLinks[i]="".join(["http://",vidLinks[i]])

			vidLinks[i]=vidLinks[i].replace('\"','').replace('\\','/').replace(" ","")

			try:
				preHash=vidLinks[i][:vidLinks[i].index("watch?")+6]
				vHash=vidLinks[i][vidLinks[i].index('v='):]
				vidLinks[i]="".join([preHash,vHash])

				if vHash in vHashList:
					vidLinks.remove(vidLinks[i])
				else:
					vHashList.append(vHash)

				try:
					vidLinks[i]=vidLinks[i][:vidLinks[i].index('&')]
				except:
					pass

			except:
				vidLinks.remove(vidLinks[i])

	return vidLinks

def alreadyDownloaded(title, targDir):
	retVal=False
	fList= listdir(targDir)
	t=path.splitext(title)[0].lower()
	for f in fList:

		if t==path.splitext(f)[0].lower():
			retVal=True
			break

	return retVal

def downloadMusic(ytVidLink, targetDir):

	command="".join([YOUTUBE_DL, ytVidLink , " --quiet --restrict-filenames --no-mtime --no-overwrites --extract-audio --output \"",targetDir,"\\%(title)s_%(id)s.%(ext)s\""])
	title=getTitleFromSys(ytVidLink)
	if len(title)>0:

		title=cleanString(title)
		if alreadyDownloaded(title, musicDir)==False:#check musicDir instead of screening dir since there's no overwrites anyway
			if path.splitext(title.lower())[0] not in deletedMusicList:
				print "Downloading:", title
				title="".join([targetDir,"\\",title])

				system(command)

				#conversion
				convertCommand="%UtilResources%/convertToMp3.py " + "\""+title+"\""
				print "Converting : ", title
				sleep(2)
				system(convertCommand)

			else:
				errorAlert( title + " already screened and deleted before" )

		else:
			errorAlert( title + " already in main music directory" )
	else:
		errorAlert( "Empty title for " + ytVidLink)

def downloadVideo(ytVidLink, targetDir):

	command="".join([YOUTUBE_DL, ytVidLink , " --quiet --rate-limit 100m  --no-mtime --no-overwrites --output \"",targetDir,"\\%(title)s_%(id)s.%(ext)s\""])
	title=getTitleFromSys(ytVidLink)

	print "Downloading:", title
	system(command)

if __name__ == "__main__":

	switchList=switchBoard(argv)
	vidList=[]

	if 's' in switchList:#single video
		print "Dowloading single video"
		vidLink=" ".join(map(str,argv[1:])).replace('\\','/')
		downloadVideo(vidLink,ytDownloadsDir)

	elif 'v' in switchList:#multiple video
		print "Downloading multiple videos from source"
		DEFAULT_LINKS=["http://www.reddit.com/r/amv"]

		if(len(argv)>1):
			DEFAULT_LINKS=argv[1:]

		vidList=getVidList(DEFAULT_LINKS)

		for vidLink in vidList:
			if(vidLink is not None):
				downloadVideo(vidLink,ytAMVDir)


	elif 'm' in switchList:#single music
		print "Downloading single music"
		deletedMusicList=open(deletedScreenedLog).read().split("\n")
		vidLink=" ".join(map(str,argv[1:])).replace('\\','/')
		downloadMusic(vidLink,musicDir)

	else:#multiple music

		DEFAULT_LINKS=["http://www.reddit.com/r/japanesemusic", "http://www.reddit.com/r/animemusic/","http://www.reddit.com/r/vocaloid"]

		if(len(argv)>1):
			DEFAULT_LINKS=argv[1:]

		vidList=getVidList(DEFAULT_LINKS)
		deletedMusicList=open(deletedScreenedLog).read().split("\n")

		for vidLink in vidList:
			if(vidLink is not None):
				#downloadMusic(vidLink,screeningDir)
				Thread(target=downloadMusic,args=(vidLink,screeningDir,)).start()
				sleep(3)