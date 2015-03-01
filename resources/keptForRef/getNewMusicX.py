"""
initTestLink:http://www.youtube.com/watch?v=xo-tWlETq8w
"""

from copy import copy
from time import sleep
from string import lower
from os import system, chdir, listdir
from threading import Thread
from bs4 import BeautifulSoup
from urlparse import urlparse
from unicodedata import normalize
from sys import argv, exit as sys_exit
from random import randint

from urllib import FancyURLopener as openURL
from psutil import get_pid_list, Process, error

from root import screeningDir, musicDir, setClipboardData, switchBoard, getAllPageLinks, ytDownloadsDir, ytAMVDir, ytAnShows, keyboardType, standardizeString
from cleanFileNames import cleanString, cleanChars
from LinkAttribute import LinkAttribute
from bs4 import BeautifulSoup, SoupStrainer

AVAILABLE_SWITCHES=['v','h','s','m']


def getVidList(DEFAULT_LINKS):
	
	vidList=[]
	for j in range(0,len(DEFAULT_LINKS)):
				
		i=0
		tempVidList=[]
		print "Retrieving video list from: ", DEFAULT_LINKS[j]
		while(len(tempVidList)==0 and i<MAX_TRIES):
			
			tempVidList=(getVidListInner(DEFAULT_LINKS[j]))
			if(len(tempVidList)==0):
				i=i+1
				print "Retry # ", i
				sleep(5)
			
			else:
				vidList.extend(tempVidList)
				
	return vidList
	
def getVidListInner(musicPageLink):
	"""
		Foreign methods: 
			from root import getAllPageLinks
			from urlparse import urlparse
			from cleanFileNames import cleanChars
	"""
	
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
	"""
		Foreign methods:
			from copy import copy
	"""
	
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
	
def getAllScript(pageSource):
	
	resultsList=BeautifulSoup(pageSource, parse_only=SoupStrainer('script'))
	resultsList=resultsList.findAll('script')

	return resultsList
	
	
def getRawDownloadLinks(blockList):
	rawResultsList=[]
	for block in blockList:
		if "\\u0026itag=18" in block or "itag%3D18" in block or "itag=18" in block or "itag=43" in block or "itag%3D43" in block or "\\u0026itag=43" in block or "\\u0026itag=34" in block or "itag%3D34" in block or "itag=34" in block :
			rawResultsList.append(block)
	return rawResultsList
	
def getRawDownloadLinks720p(blockList):
	rawResultsList=[]
	for block in blockList:
		if "\\u0026itag=22" in block or "itag%3D22" in block or "itag=22" in block or "\\u0026itag=45" in block or "itag%3D45" in block or "itag=45" in block :
			rawResultsList.append(block)
	return rawResultsList
	
def getScriptBlock(scriptList):
	resultScript=""
	for script in scriptList:
		if "itag=18" in script.text:
			resultScript=script.text
			break
					
	return resultScript
	

def htmlManualDecode(link):
		
	try:
		returnVal=link.replace("%253A",":").replace("%252F","/").replace("%253F","?").replace("%25252C",",").replace("%3D","=").replace("%26","&").replace("%253D","=").replace("%2526","&").replace("%253B",";").replace("%2B"," ").replace("%2522","\"").replace("%252C",",").replace(" ","%20").replace("\"","%22").replace("%2C","&").replace("%3A",':').replace("%2F",'/').replace("\\u0026",'&').replace("%3F",'?')
	except AttributeError:
		returnVal=None
		
	
	return returnVal
	

	
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
	"""EXTRACTS audio (mka) from the mp4 file and then deletes the mp4 file. Doesn't actually "convert" """
	print "Beginning conversion of: ", fileTitle
		
	outputName="".join([chosenDir,"\\",fileTitle[:fileTitle.rindex('.')],".mka"])#uMad?
	inputName="".join([chosenDir,"\\",fileTitle])
	
	convertCommand="".join(["\"", "\"C:\\Program Files (x86)\\MKVToolNix\\mkvmerge.exe\"", " -o ", "\"", outputName, "\"",  " \"--forced-track\" ","\"0:no\"", " \"-a\" ", "\"0\"",  " \"-D\" ", "\"-S\"",  " \"-T\" ", "\"--no-global-tags\"", " \"--no-chapters\" ", " \"(\" \"", inputName,"\" \")\" ", " \"--track-order\" ", " \"0:0\" ", "\""])
	
	#print convertCommand
	#print "0:0 =", system(convertCommand)
	
	if system(convertCommand)==2:
		convertCommand="".join(["\"", "\"C:\\Program Files (x86)\\MKVToolNix\\mkvmerge.exe\"", " -o ", "\"", outputName, "\"",  " \"--forced-track\" ","\"1:no\"", " \"-a\" ", "\"1\"",  " \"-D\" ", "\"-S\"",  " \"-T\" ", "\"--no-global-tags\"", " \"--no-chapters\" ", " \"(\" \"", inputName,"\" \")\" ", " \"--track-order\" ", " \"0:1\" ", "\""])
		
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


	
	
def getDownloadLink(linkAttrib,quality):
	
	#condition 1: gcr
	if len(linkAttrib.gcr)>0:
		linkAttrib.sparams="&sparams=cp,gcr,id,ip,ipbits,itag,ratebypass,source,upn,expire"
	else:
		linkAttrib.sparams="&sparams=cp,id,ip,ipbits,itag,ratebypass,source,upn,expire"
	
	#condition 2: ratebypass
	
	if len(linkAttrib.ratebypass)==0:
		linkAttrib.ratebypass="&ratebypass=yes"

	
	#condition 3: check for ',' extending signature
	
	if ',' in linkAttrib.signature:
		comaLoc=linkAttrib.signature.index(',')
		sigLoc=linkAttrib.signature.index("signature")
		if comaLoc < sigLoc :
			linkAttrib.signature=linkAttrib.signature[comaLoc+1 :]
		else:
			linkAttrib.signature=linkAttrib.signature[:comaLoc]
		
	if '&' not in linkAttrib.signature:
		linkAttrib.signature="".join(['&',linkAttrib.signature])
	

	#condition 4: itag connect be in videoplayback
	
	if "itag" in linkAttrib.videoplayback:
		linkAttrib.videoplayback=linkAttrib.videoplayback[:linkAttrib.videoplayback.index('?')]
		linkAttrib.ip=linkAttrib.ip.replace('&','?')
	
	if quality=="480p":
		linkAttrib.itag="&itag=18"
	elif quality=="720p":
		linkAttrib.itag="&itag=22"
	else:
		print "Unknown quality: ", quality
		raise TypeError
	
	
	
	return "".join([linkAttrib.videoplayback,linkAttrib.ip,linkAttrib.sver,linkAttrib.expire,linkAttrib.key,linkAttrib.source,linkAttrib.mv,linkAttrib.upn,linkAttrib.ms,linkAttrib.mt,linkAttrib.fexp,linkAttrib.id,linkAttrib.gcr,linkAttrib.sparams,linkAttrib.ipbits,linkAttrib.cp,linkAttrib.signature,linkAttrib.itag,linkAttrib.ratebypass]).strip()
	
def downloadMusic(ytLink, dirLocation, convert=True):
	
	
	#Start
	
	pageSource=getPageSource(ytLink)
	scriptList=getAllScript(pageSource)
	resultScript=getScriptBlock(scriptList)
	urlBlockList= resultScript.split("\\u0026url=")
	rawLinkList=getRawDownloadLinks(urlBlockList)
	
	fileTitle=getFileTitle(pageSource,ytLink)
	fileTitle=cleanString(fileTitle)
	
	chdir(dirLocation)
	
	fileTitle=checkIfAlreadyDownloaded(fileTitle, dirLocation)
	
	for rawLink in rawLinkList:
		
		decodedLink=htmlManualDecode(rawLink)
		linkAttrib=LinkAttribute(decodedLink)
		
		downloadLink=getDownloadLink(linkAttrib,"480p")
		print "\nDownloading: ", fileTitle
		command="".join(["wget --tries=3 -q ", "\"", downloadLink, "\"", " -O ", "\"", fileTitle, "\""  ])
		
		if system(command)==0 and convert==True:
			convertToMp3(fileTitle,dirLocation)
			break
	
	
	#system("wget -q \"http://o-o---preferred---sn-ni5f-ttje---v17---lscache4.c.youtube.com/videoplayback?upn=OmAyI1JhUvo&sparams=cp,id,ip,ipbits,itag,ratebypass,source,upn,expire&fexp=921007,919350,922401,920704,912806,913419,913558,913556,919351,925109,919003,912706&key=yt1&expire=1348534246&itag=18&ipbits=8&sver=3&ratebypass=yes&mt=1348511892&ip=174.5.137.168&mv=m&source=youtube&ms=au&cp=U0hTTVVOUl9JUENOM19NSFZDOnlja2xkV0I4eGtx&id=9dfe7e3ebc75f593&newshard=yes&type=video/mp4;codecs=\"avc1.42001E,mp4a.40.2\"&fallback_host=tc.v5.cache7.c.youtube.com&signature=7006222DBD71CBEE19A02B20340B54E7BCDB4491.29F419BA1B58EBF80452682E38F379E45D697084&keepalive=yes\" -O \"The Next Big Thing is Already Here -- Samsung Galaxy S III.mp4\"")


def checkIfAlreadyDownloaded(fName, dirLocation):
	locNameList=listdir(dirLocation)
	renamedFile=fName
	for locName in locNameList:
		if standardizeString(fName)==standardizeString(locName):
			renamedFile="".join([fName.replace(".mp4",""),"_",str(randint(0,999)),".mp4"])
			print fName, " is already downlodaded.", " Renaming file to ", renamedFile
			break
	return renamedFile
			

def download720yt(ytLink, dirLocation=ytAMVDir):
	
	#check if filename is already downloaded
	pageSource=getPageSource(ytLink)
	scriptList=getAllScript(pageSource)
	resultScript=getScriptBlock(scriptList)
	urlBlockList= resultScript.split("\\u0026url=")
	rawLinkList=getRawDownloadLinks720p(urlBlockList)
	
	fileTitle=getFileTitle(pageSource,ytLink)
	fileTitle=cleanString(fileTitle)
	
	chdir(dirLocation)
	
	fileTitle=checkIfAlreadyDownloaded(fileTitle, dirLocation)
	
	for rawLink in rawLinkList:
		
		decodedLink=htmlManualDecode(rawLink)
		linkAttrib=LinkAttribute(decodedLink)
		
		downloadLink=getDownloadLink(linkAttrib,"720p")
		print "\nDownloading: ", fileTitle
		command="".join(["wget --tries=3 -q ", "\"", downloadLink, "\"", " -O ", "\"", fileTitle, "\""  ])
		
		if system(command)==0:
			break

def cleanYT(str):
	
	
	if "http//:" in str:
		cleaned=str.replace("http//:","http://")
	else:
		cleaned=str
		
	try:
		cleaned=cleaned[:cleaned.index('&')]
	except ValueError:
		pass
		
	return cleaned
	
	
def prepDownload(vidList,selectedDir):
	
	deleteDuplicates(vidList)
	cleanVidList(vidList)
	
	for i in range(0,len(vidList)):		
			
		if (i+1)%15==0:
			waitForWget()
		
		else:
			if selectedDir==ytAMVDir or selectedDir==ytDownloadsDir:				
				Thread(target=download720yt,args=(cleanYT(vidList[i]),selectedDir,)).start()
				
			elif selectedDir==screeningDir or selectedDir==musicDir:
				Thread(target=downloadMusic,args=(cleanYT(vidList[i]),selectedDir,)).start()
						
			sleep(3)
	
	waitForWget()
	
if __name__ == "__main__":
	
	MAX_TRIES=3
	
	switchList=switchBoard(argv)
	vidList=[]
	
	
	if 's' in switchList:#single video 720p
		
		for arg in argv:
			vidList.append(arg.replace('\\','/'))
		
		prepDownload(vidList,ytDownloadsDir)
		
	elif 'm480' in switchList:#multipleVideo at 480p
		print "Downloading multiple videos at 480p."
		DEFAULT_LINKS=argv[1:].replace('\\','/')
		
		if len(DEFAULT_LINKS)>0:
			vidList=getVidList(DEFAULT_LINKS)
			deleteDuplicates(vidList)
			cleanVidList(vidList)
			for i in range(0,len(vidList)):	
				
				if (i+1)%15==0:
					waitForWget()
					
				else:
					Thread(target=downloadMusic,args=(cleanYT(vidList[i]),ytAnShows,False,)).start()
		else:
			print "Missing video link argument"
			
	elif 's480' in switchList:
		print "Downloading single video in 480p."
		ytLink=argv[1].replace('\\','/')
		Thread(target=downloadMusic,args=(cleanYT(ytLink),ytDownloadsDir,False,)).start()
		
	elif 'v' in switchList:#multiple videos- 720p
		
		DEFAULT_LINKS=["http://www.reddit.com/r/amv"]
		
		if(len(argv)>1):
			vidList=getVidList(argv[1:])
		else:
			vidList=getVidList(DEFAULT_LINKS)
			
		prepDownload(vidList,ytAMVDir)
		
	
	elif 'm' in switchList:#single music
		for arg in argv:
			vidList.append(arg.replace('\\','/'))
		prepDownload(vidList,musicDir)
	
	else:#multiple music
		DEFAULT_LINKS=["http://www.reddit.com/r/dubstep","http://www.reddit.com/r/japanesemusic", "http://www.reddit.com/r/animemusic/","http://www.reddit.com/r/vocaloid"]
		
		if(len(argv)>1):
			vidList=getVidList(argv[1:])
		else:
			vidList=getVidList(DEFAULT_LINKS)	
		
			
			
		prepDownload(vidList,screeningDir)
		
		system("%UtilResources%/cleanFileNames.pyc \"C:/Users/Kevin/Music/ytcon/screen\" ")
	


	
