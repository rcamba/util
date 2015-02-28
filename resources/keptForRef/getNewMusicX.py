"""
initTestLink:http://www.youtube.com/watch?v=xo-tWlETq8w
"""

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

from root import screeningDir, musicDir, setClipboardData, switchBoard, getAllPageLinks, ytDownloadsDir, ytAMVDir, ytAnShows, keyboardType
from cleanFileNames import cleanString, cleanChars
from LinkAttribute import LinkAttribute
from mouseMacro import move, click

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
	

def get_URL_BlockList(pageSource):
	return pageSource.split("url%3D")[:-1]
	

def htmlManualDecode(link):
		
	try:
		returnVal=link.replace("%253A",":").replace("%252F","/").replace("%253F","?").replace("%25252C",",").replace("%3D","=").replace("%26","&").replace("%253D","=").replace("%2526","&").replace("%253B",";").replace("%2B"," ").replace("%2522","\"").replace("%252C",",").replace(" ","%20").replace("\"","%22").replace("%2C","&")
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


	
	
def getDownloadLink(cleanedLink, gItag):
	#decomposition
	
	linkAttrib=LinkAttribute()
	
	attributeList=cleanedLink.split('&')
	finalLink=attributeList[0]		
	attributeList=attributeList[1:]
	
	for i in range(len(attributeList)-1,-1,-1):
		if len(attributeList[i])>0:
			attributeList[i]=str("".join(["&",attributeList[i]]))
			linkAttrib.addAttrib(attributeList[i])
	
	#recomposition
	linkAttrib.itag=gItag
	recomposed="".join([linkAttrib.itag, linkAttrib.sparams, linkAttrib.algorithm, linkAttrib.burst, linkAttrib.id, linkAttrib.expire, linkAttrib.fexp, linkAttrib.ip, linkAttrib.upn, linkAttrib.cp, linkAttrib.ipbits, linkAttrib.newshard, linkAttrib.key, linkAttrib.ms, linkAttrib.ratebypass, linkAttrib.source, linkAttrib.sver, linkAttrib.mv, linkAttrib.mt, linkAttrib.signature, linkAttrib.fallback, linkAttrib.type, linkAttrib.gcr])
	
	"""	http://r7---sn-ni5f-ttjl.c.youtube.com/videoplayback?expire=1356567114&id=048e5bfb4e45781d&sparams=cp,id,ip,ipbits,itag,ratebypass,source,upn,expire&fexp=916602,906071,914005,916624,920704,912806,928001,922403,922405,929901,913605,929104,913546,913556,908496,920201,913302,919009,911116,926403,901451,902556&ip=174.5.137.168&upn=-6UMUVhXpHM&cp=U0hUS1VRVV9GTkNONF9NS1lCOmJkVWsxcmRiNl9N&ipbits=8&newshard=yes&itag=37&key=yt1&ms=au&ratebypass=yes&source=youtube&sver=3&mv=m&mt=1356544692&signature=36ED6FB72DF44244D4004AB4C955793119EF33D4.579C1FB75B1A24063DD22F0F374FD446C94F8168&fallback_host=tc.v10.cache4.c.youtube.com&type=video/mp4;%20codecs=%22avc1.64001F,%20mp4a.40.2%22
	"""
	
	return "".join([finalLink, recomposed])
	
def downloadMusic(ytLink, dirLocation, convert=True):
	
	def cleanMP4Link(mp4Link):
	
		def cleanSliceEnd(link):
			if link!=None:
				sigReplace=link.replace("sig","signature")
				sigSlice="".join( [sigReplace[:sigReplace.index("&quality=medium")], "&keepalive=yes" ])	
			else:
				sigSlice=None
				
			return sigSlice
		
		cleanedHTML=htmlManualDecode(mp4Link)
		fullyCleaned=cleanSliceEnd(cleanedHTML)
		
		return fullyCleaned
		
	def getMP4Link(blockList):
		result=None
		for block in blockList:
			if "medium" in block and "mp4" in block:
				result=block
				break
				
		return result
	#Start
	
	pageSource=getPageSource(ytLink)
	URL_BlockList=get_URL_BlockList(pageSource)
	mp4Link=getMP4Link(URL_BlockList)
	cleanedLink=htmlManualDecode(mp4Link)
	cleanedLink=cleanedLink.replace("sig","signature").replace("&quality=medium","")
	#downloadLink=getDownloadLink(cleanedLink, "&itag=18")
	print cleanedLink
	exit()
	#downloadLink=cleanMP4Link(mp4Link)
	
	
	if downloadLink!=None:
		downloadLink=downloadLink.replace(' ','')
		
		fileTitle=getFileTitle(pageSource,ytLink)
		print "\nDownloading: ", fileTitle
		
		fileTitle=cleanString(fileTitle)
		print "Cleaning filename. Cleaned to: ", fileTitle
		
		chdir(dirLocation)
		
		command="".join(["wget -q ","\"",downloadLink,"\""," -O ","\"",fileTitle,"\""])
		print system(command)
		
		if convert==True:
			convertToMp3(fileTitle,dirLocation)
	
	else:
		print "Invalid download link. Skipping: ", ytLink
	
	#system("wget -q \"http://o-o---preferred---sn-ni5f-ttje---v17---lscache4.c.youtube.com/videoplayback?upn=OmAyI1JhUvo&sparams=cp,id,ip,ipbits,itag,ratebypass,source,upn,expire&fexp=921007,919350,922401,920704,912806,913419,913558,913556,919351,925109,919003,912706&key=yt1&expire=1348534246&itag=18&ipbits=8&sver=3&ratebypass=yes&mt=1348511892&ip=174.5.137.168&mv=m&source=youtube&ms=au&cp=U0hTTVVOUl9JUENOM19NSFZDOnlja2xkV0I4eGtx&id=9dfe7e3ebc75f593&newshard=yes&type=video/mp4;codecs=\"avc1.42001E,mp4a.40.2\"&fallback_host=tc.v5.cache7.c.youtube.com&signature=7006222DBD71CBEE19A02B20340B54E7BCDB4491.29F419BA1B58EBF80452682E38F379E45D697084&keepalive=yes\" -O \"The Next Big Thing is Already Here -- Samsung Galaxy S III.mp4\"")



def download720yt(ytLink, dirLocation=ytAMVDir):
	
	def clean720pLink(link720):
		
		def cleanSliceEnd(link):
			if link!=None:
				sigReplace=link.replace("sig","signature")
				sigSlice="".join( [sigReplace[:sigReplace.index("&quality=hd720")], "&keepalive=yes"])
			else:
				sigSlice=None
			return sigSlice
	
		fullyCleaned=cleanSliceEnd(link720)
		
		return fullyCleaned
	
	def get720Link(blockList):
		result=None
		
		for block in blockList:
			
			if "hd720" in block in block and "mp4" in block :
				result=block
				break

		return result
		
	
	
	#Start
	
	pageSource=getPageSource(ytLink)
	URL_BlockList=get_URL_BlockList(pageSource)
	mp4Link=get720Link(URL_BlockList)
	cleanedLink=htmlManualDecode(mp4Link)
	
	downloadLink=getDownloadLink(cleanedLink,"&itag=22")
	
	#downloadLink=clean720pLink(mp4Link)
	
	
	
	if downloadLink!=None:
		downloadLink=downloadLink.replace(' ','')
		
		fileTitle=getFileTitle(pageSource,ytLink).replace("quot;","").replace("&","").replace("?","")
		print "Downloading: ", fileTitle
		
		fileTitle=cleanString(fileTitle)
		print "Cleaning filename. Cleaned to: ", fileTitle
		
		chdir(dirLocation)
		
		command="".join(["wget -q","\"",downloadLink,"\""," -O ","\"",fileTitle,"\""])
		print system(command)
		
	else:
		print "Invalid download link. Skipping: ", downloadLink
	

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
	
if __name__ == "__main__":
	
	MAX_TRIES=3
	
	switchList=switchBoard(argv)
	vidList=[]
	
	
	if 's' in switchList:#single video 720p
		
		for arg in argv:
			vidList.append(arg.replace('\\','/'))
		
		prepDownload(vidList,ytDownloadsDir)
		
	elif 'm480' in switchList:#multipleVideo at 480p
		print "Downloading videos at 480p"
		DEFAULT_LINKS=["http://www.youtube.com/playlist?list=PLfvarqT_23pWuc6D8nYWYWIh3vJ_Ewq7z"]#argv[1:]
		
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
		
		ytLink=argv[1].replace('\\','/')
		#downloadMusic(cleanYT(ytLink),ytAnShows,False)
		Thread(target=downloadMusic,args=(cleanYT(ytLink),ytAnShows,False,)).start()
		
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
		DEFAULT_LINKS=[
		"http://www.reddit.com/r/japanesemusic", "http://www.reddit.com/r/animemusic/"]#"http://www.reddit.com/r/vocaloid",
		
		if(len(argv)>1):
			vidList=getVidList(argv[1:])
		else:
			vidList=getVidList(DEFAULT_LINKS)	
		deleteDuplicates(vidList)
		cleanVidList(vidList)
		counter=0
		
		for vid in vidList:
			system("firefox -new-tab " + "\"" +vid + "\"")
			sleep(7)
			keyboardType("{ENTER}")
			
			sleep(3)
			keyboardType("{ENTER}")
			sleep(3)
			system("kill FlashPlayerPlugin_11_5_502_135")
			counter+=1
			if counter%15==0:
				print "Starting sleep"
				sleep(300)
			
		#prepDownload(vidList,screeningDir)
		
		#system("%UtilResources%/cleanFileNames.pyc \"C:/Users/Kevin/Music/ytcon/screen\" ")
	


	
