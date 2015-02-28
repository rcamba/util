from urllib import FancyURLopener as openURL
from os import getenv, system
from sys import path
path.insert(0,getenv("UtilResources"))

from LinkAttribute import *
from bs4 import BeautifulSoup
from unicodedata import normalize

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

def getPageSource(link):
	return openURL({}).open(link).read()
def get_preload_BlockList(pageSource):
	return pageSource.split("yt.preload.start")

	
def getAllScript(pageSource):
	from bs4 import BeautifulSoup, SoupStrainer
	resultsList=BeautifulSoup(pageSource, parse_only=SoupStrainer('script'))
	resultsList=resultsList.findAll('script')
	

	return resultsList

def getScriptBlock(scriptList):
	for script in scriptList:
		if "itag=18" in script.text:
			resultScript=script.text
			break
					
	return resultScript

def getRawDownloadLinks(blockList):
	rawResultsList=[]
	for block in blockList:
		if "\\u0026itag=18" in block or "itag%3D18" in block or "itag=18" in block or "itag=43" in block or "itag%3D43" in block or "\\u0026itag=43" in block or "\\u0026itag=34" in block or "itag%3D34" in block or "itag=34" in block :
			rawResultsList.append(block)
			
			
			
	return rawResultsList
	
def htmlManualDecode(link):
		
	try:
		returnVal=link.replace("%253A",":").replace("%252F","/").replace("%253F","?").replace("%25252C",",").replace("%3D","=").replace("%26","&").replace("%253D","=").replace("%2526","&").replace("%253B",";").replace("%2B"," ").replace("%2522","\"").replace("%252C",",").replace(" ","%20").replace("\"","%22").replace("%2C","&").replace("%3A",':').replace("%2F",'/').replace("\\u0026",'&').replace("%3F",'?')
	except AttributeError:
		returnVal=None
		
	
	return returnVal
	
def getDownloadLink(linkAttrib):
	
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
		if linkAttrib.signature[0]==',':
			linkAttrib.signature=linkAttrib.signature[1:]
		else:
			linkAttrib.signature=linkAttrib.signature[:linkAttrib.signature.index(',')]
	
	
	linkAttrib.itag="&itag=18"
	
	
	
	
	return "".join([linkAttrib.videoplayback,linkAttrib.ip,linkAttrib.sver,linkAttrib.expire,linkAttrib.key,linkAttrib.source,linkAttrib.mv,linkAttrib.upn,linkAttrib.ms,linkAttrib.mt,linkAttrib.fexp,linkAttrib.id,linkAttrib.gcr,linkAttrib.sparams,linkAttrib.ipbits,linkAttrib.cp,linkAttrib.signature,linkAttrib.itag,linkAttrib.ratebypass]).strip()
	

			
def downloadMusic(ytLink,convert=True): #480p
	
	
	pageSource=getPageSource(ytLink)
	scriptList=getAllScript(pageSource)
	resultScript=getScriptBlock(scriptList)


	urlBlockList= resultScript.split("\\u0026url=")
	
	
	rawLinkList=getRawDownloadLinks(urlBlockList)
	fileTitle=getFileTitle(pageSource,ytLink)
	for rawLink in rawLinkList:
		decodedLink=htmlManualDecode(rawLink)
		linkAttrib=LinkAttribute(decodedLink)
		
		downloadLink=getDownloadLink(linkAttrib)
		command="".join(["wget ", "\"", downloadLink, "\"", " -O ", "\"", fileTitle, "\""  ])
		
		print system(command)
		#break

if __name__=="__main__":
	#downloadMusic("http://www.youtube.com/watch?v=wup7peCB0E0")
	#downloadMusic("https://www.youtube.com/watch?v=2XF_bYII1sE")
	downloadMusic("https://www.youtube.com/watch?v=_0kpRNJpmOw")



#bob=cleaned.replace("\\u0026",'&').replace("%3A",':').replace("%2F",'/').replace("sparams=algorithm,burst,cp,factor,gcr,id,ip,ipbits,itag,source,upn,expire","sparams=cp,gcr,id,ip,ipbits,itag,ratebypass,source,upn,expire").replace("&algorithm=throttle-factor","").replace("&burst=40","").replace("&factor=1.25","").replace("sig","signature").replace("%3F",'?').replace("algorithm=throttle-factor","")



#http://r1---sn-ni5f-ttje.c.youtube.com/videoplayback?ip=174.5.137.168&sver=3&expire=1356989295&key=yt1&source=youtube&mv=m&upn=f6YZCzxnP54&ms=au&mt=1356964632&fexp=927101,906376,927903,911614,914050,916612,920704,912806,928001,922403,922405,929901,913605,929104,913546,913556,908496,920201,913302,919009,911116,901451,902556&id=532590dd940414bc&gcr=ca&sparams=cp,gcr,id,ip,ipbits,itag,ratebypass,source,upn,expire&ipbits=8&cp=U0hUS1lTV19OT0NONF9RTUFDOkpROTNNWV9xeHNC&newshard=yes&signature=64A83DEF4BDC32811A9F430E0E7A3985BDC8DA8E.8BFBBB892D62866832BA351525AFD863C4DB66A9&itag=18&ratebypass=yes
#print r[len(r)-1].replace("&",'&').replace("generate_204","videoplayback")

"""









itag: 22 , width: 1280, height: 720, container: "MP4" , acodec:"AAC" , vcodec: "H.264" , vprofile: "High" , level: 3.1 },
{ itag: 45 , width: 1280, height: 720, container: "WebM", acodec:"Vorbis", vcodec: "VP8" },

{ itag: 18 , width: 640, height: 360, container: "MP4" , acodec:"AAC" , vcodec: "H.264" , vprofile: "Baseline", level: 3.0 },
{ itag: 34 , width: 640, height: 360, container: "FLV" , acodec:"AAC" , vcodec: "H.264" , vprofile: "Main" , level: 3.0 },
{ itag: 43 , width: 640, height: 360, container: "WebM", acodec:"Vorbis", vcodec: "VP8" },









TvP notes
7 minute build second CC
3 marines + bunker and then reactor on racks
get 1 tank, then 1 banshee 
harass with just 1 banshee no cloak
then get siege
"""


