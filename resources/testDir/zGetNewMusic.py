"""http://www.youtube.com/watch?v=xo-tWlETq8w"""

from copy import copy
from time import sleep
from string import lower
from os import system, chdir
from threading import Thread
from bs4 import BeautifulSoup
from urlparse import urlparse
from unicodedata import normalize
from sys import argv, exit as sys_exit

from urllib import FancyURLopener as openURL
from psutil import get_pid_list, Process, error

from root import screeningDir, musicDir, setClipboardData, switchBoard, getAllPageLinks
from cleanFileNames import cleanChars

AVAILABLE_SWITCHES=['v','h']

def getVidList(musicPageLink):
		
	musicPageLink=musicPageLink.replace('\\','/')
	allPageLinks=getAllPageLinks(musicPageLink)
	scheme=urlparse(musicPageLink)[0]
	netloc=urlparse(musicPageLink)[1]
	
	vidList=[]
	
	if netloc=="www.youtube.com":
		for link in allPageLinks:
			try:
				target=str(link.get("href"))
			except UnicodeEncodeError:
				target=cleanChars(target)
				
			if(type(target)==str):
				
				if "watch" in target:
					target="".join([scheme,"//:",netloc,target])#assume scheme is "http" since no case of www yet
					vidList.append(target)
	else:
		for link in allPageLinks:
			
			try:
				target=str(link.get("href"))
			except UnicodeEncodeError:
				target=cleanChars(target)
			
			if(type(target)==str):
				if "youtube" in target or "youtu.be" in target:
					vidList.append(target)
				
	return vidList
	
def deleteDuplicates(locList):
	
	comparativeList=copy(locList)
	
	for i in range(len(locList)-1,-1,-1):
		
		comparativeList.remove(locList[i])
		if(locList[i] in comparativeList):
			locList.remove(locList[i])		
def cleanVidList(vidList):
	"""removes invalid link; non-direct youtube links"""
	
	for vidLink in vidList:
		
		youtubeLink=vidLink.replace('\"','').replace('\\','/')
		
		if "www." in youtubeLink:
			youtubeLink="".join([ "http://", youtubeLink[youtubeLink.index('.')+1:] ])
		
		netloc=urlparse(youtubeLink)[1]	
		
		if netloc!="www.youtube.com" and netloc!="www.youtu.be" and netloc!="youtube.com" and netloc!="youtu.be" :
			#print youtubeLink, " is not from youtube.com"
			#print "netloc is: ", netloc
			vidList.remove(vidLink)
				
		elif "playlist" in lower(youtubeLink):
			vidList.remove(vidLink)
			
def getPageSource(link):
	return openURL({}).open(link).read()
	

def get_URL_BlockList(pageSource):
	return pageSource.split("url%3D")
	
def getMP4Link(blockList):
	result=None
	for block in blockList:
		if "medium" in block and "mp4" in block:
			result=block
			break
			
	return result
	
def get720Link(blockList):
	result=[]
	for block in blockList:
		if "hd720" in block and "mp4" in block and "itag%3D44" in block:
			result=block
			break
	
	return result
	

	
def cleanMP4Link(mp4Link):
	def htmlManualDecode(link):
		return link.replace("%253A",":").replace("%252F","/").replace("%253F","?").replace("%25252C",",").replace("%3D","=").replace("%26","&").replace("%253D","=").replace("%2526","&").replace("%253B",";").replace("%2B"," ").replace("%2522","\"").replace("%252C",",")
		
	def cleanSliceEnd(link):
		sigReplace=link.replace("sig","signature")
		sigSlice="".join( [sigReplace[:sigReplace.index("&quality=medium")], "&keepalive=yes" ])		
		
		return sigSlice
	
	cleanedHTML=htmlManualDecode(mp4Link)
	fullyCleaned=cleanSliceEnd(cleanedHTML)
	
	
	return fullyCleaned
	
def clean720pLink(link720):
	def htmlManualDecode(link):
		return link.replace("%253A",":").replace("%252F","/").replace("%253F","?").replace("%25252C",",").replace("%3D","=").replace("%26","&").replace("%253D","=").replace("%2526","&").replace("%253B",";").replace("%2B"," ").replace("%2522","\"").replace("%252C",",")
		
	def cleanSliceEnd(link):
		sigReplace=link.replace("sig","signature")
		sigSlice="".join( [sigReplace[:sigReplace.index("&quality=hd720")], "&keepalive=yes" ])
		
		return sigSlice
	
	cleanedHTML=htmlManualDecode(link720)
	fullyCleaned=cleanSliceEnd(cleanedHTML)
	
	
	return fullyCleaned
	
def getFileTitle(pageSource, youtubeLink):
	
	soup=BeautifulSoup(pageSource)
	origTitle = soup.html.head.title.text
	origTitle=str(normalize('NFKD', origTitle).encode('ascii','ignore').replace("\n","").replace("- YouTube","").strip())
	fTitle=origTitle.replace('/','').replace('\\','').replace(':','').replace('|','')
	#chars that wget can't handle as part of file title
	
	fTitle="".join([fTitle,".mp4"])
	

	while(fTitle[0].isalnum()==False and fTitle[0]!='['):
		fTitle=fTitle[1:]

		if(fTitle=="mp4"):
			print "Empty file title."
			#print "Original file name: ", origTitle
			print "Temporarily renamed to : V_" , youtubeLink[youtubeLink.rindex('='):].replace('=','').replace('/','').replace('\\','').strip()
			print "YT link: ", youtubeLink
			#fTitle=raw_input("Enter a new file title:\n")
			fTitle="".join(["V_",youtubeLink[youtubeLink.rindex('='):].replace('=','').replace('/','').replace('\\',''),".mp4"])
	
	return fTitle

def convertToMp3(fileTitle, chosenDir):
	
	print "Beginning conversion of: ", fileTitle
		
	outputName="".join([chosenDir,"\\",fileTitle[:fileTitle.rindex('.')],".mka"])#uMad?
	inputName="".join([chosenDir,"\\",fileTitle])
	
	convertCommand="".join(["\"", "\"C:\\Program Files\\MKVToolNix\\mkvmerge.exe\"", " -o ", "\"", outputName, "\"",  " \"--forced-track\" ","\"0:no\"", " \"-a\" ", "\"0\"",  " \"-D\" ", "\"-S\"",  " \"-T\" ", "\"--no-global-tags\"", " \"--no-chapters\" ", " \"(\" \"", inputName,"\" \")\" ", " \"--track-order\" ", " \"0:0\" ", "\""])
	
	#print convertCommand
	#print "0:0 =", system(convertCommand)
	
	if system(convertCommand)==2:
		convertCommand="".join(["\"", "\"C:\\Program Files\\MKVToolNix\\mkvmerge.exe\"", " -o ", "\"", outputName, "\"",  " \"--forced-track\" ","\"1:no\"", " \"-a\" ", "\"1\"",  " \"-D\" ", "\"-S\"",  " \"-T\" ", "\"--no-global-tags\"", " \"--no-chapters\" ", " \"(\" \"", inputName,"\" \")\" ", " \"--track-order\" ", " \"0:1\" ", "\""])
		
		#print convertCommand
		print "0:1 = ", system(convertCommand)
		
	system("".join(["del ","\"",inputName,"\""]))	
	
def waitForWget():
	"""Views all currently running processes and stores wget.exe(s) into list
	Then iterates through list and checks if PID of wget still exists (i.e still running)
	If it is then
		sleep for 30 seconds and wait for it to finish
	Else
		move to next element until end of list
	"""
		
	print "Waiting for wGet to finish"
	wgetPidList=[]
	pidList=list(get_pid_list())
	for i in range(0,len(pidList)):
		try:
			if(lower(Process(pidList[i]).name)=="wget.exe"):
				wgetPidList.append(pidList[i])
		except error.NoSuchProcess:
			print "Process with PID: ", pidList[i], " not found."
	
	#print wgetPidList
	for i in range(0,len(wgetPidList)):
		while(wgetPidList[i] in pidList):
			pidList=list(get_pid_list())
			sleep(30)

	print "wGet is finished."

def mainMethod(ytLink, dirLocation):
	
	pageSource=getPageSource(ytLink)
	URL_BlockList=get_URL_BlockList(pageSource)
	mp4Link=getMP4Link(URL_BlockList)
	downloadLink=cleanMP4Link(mp4Link)
	fileTitle=getFileTitle(pageSource,ytLink).replace("quot;","").replace("&","").replace("?","")
	print "Downloading: ", fileTitle
	
	downloadLink=downloadLink.replace(' ','')
	
	chdir(dirLocation)
	
	command="".join(["wget -q ","\"",downloadLink,"\""," -O ","\"",fileTitle,"\""])
	print system(command)
	
	
	if(dirLocation==screeningDir or dirLocation==musicDir):
		convertToMp3(fileTitle,dirLocation)
	
	
	#system("wget -q \"http://o-o---preferred---sn-ni5f-ttje---v17---lscache4.c.youtube.com/videoplayback?upn=OmAyI1JhUvo&sparams=cp,id,ip,ipbits,itag,ratebypass,source,upn,expire&fexp=921007,919350,922401,920704,912806,913419,913558,913556,919351,925109,919003,912706&key=yt1&expire=1348534246&itag=18&ipbits=8&sver=3&ratebypass=yes&mt=1348511892&ip=174.5.137.168&mv=m&source=youtube&ms=au&cp=U0hTTVVOUl9JUENOM19NSFZDOnlja2xkV0I4eGtx&id=9dfe7e3ebc75f593&newshard=yes&type=video/mp4;codecs=\"avc1.42001E,mp4a.40.2\"&fallback_host=tc.v5.cache7.c.youtube.com&signature=7006222DBD71CBEE19A02B20340B54E7BCDB4491.29F419BA1B58EBF80452682E38F379E45D697084&keepalive=yes\" -O \"The Next Big Thing is Already Here -- Samsung Galaxy S III.mp4\"")
	
if __name__ == "__main__":
	
	MAX_TRIES=3
	DEFAULT_LINKS=["http://www.reddit.com/r/vocaloid","http://www.reddit.com/r/dubstep"]
	switchList=switchBoard(argv)
	if(len(argv)>1):
		DEFAULT_LINKS=argv[1:]
	
	for j in range(0,len(DEFAULT_LINKS)):
		
		i=0
		vidList=[]
		print "Retrieving video list from: ", DEFAULT_LINKS[j]
		while(len(vidList)==0 and i<MAX_TRIES):
			
			vidList=getVidList(DEFAULT_LINKS[j])
			if(len(vidList)==0):
				i=i+1
				print "Retry # ", i
				sleep(5)
		
		deleteDuplicates(vidList)
		cleanVidList(vidList)
		#print vidList
		#print "Number of videos:", len(vidList)
		
		if "v" not in switchList:
			selectedDir=screeningDir
		else:
			selectedDir=musicDir
	
		for vidLink in vidList:		
			Thread(target=mainMethod,args=(vidLink,selectedDir,)).start()
			sleep(3)
	

	waitForWget()
	system("%UtilResources%/cleanFileNames.pyc \"C:/Users/Kevin/Music/ytcon/screen\" ")
	
	
def download720yt(ytLink, dirLocation="C:\\Users\\Kevin\\Videos"):
	
	pageSource=getPageSource(ytLink)
	URL_BlockList=get_URL_BlockList(pageSource)
	mp4Link=get720Link(URL_BlockList)
	downloadLink=clean720pLink(mp4Link)
	fileTitle=getFileTitle(pageSource,ytLink).replace("quot;","").replace("&","").replace("?","")
	print "Downloading: ", fileTitle
	
	downloadLink=downloadLink.replace(' ','')
	
	chdir(dirLocation)
	
	command="".join(["wget -q ","\"",downloadLink,"\""," -O ","\"",fileTitle,"\""])
	print system(command)