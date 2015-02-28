"""
t1:http://www.youtube.com/watch?v=GfGeSwLZhBQ; title only
t2:http://www.youtube.com/watch?v=u-d3hI0GCV8; title + vidID
t3:http://www.youtube.com/watch?v=xo-tWlETq8w; restricted download
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
from urllib import unquote_plus
from urllib import FancyURLopener as openURL
from psutil import get_pid_list, Process, error
import subprocess

from root import screeningDir, musicDir, setClipboardData, switchBoard, getAllPageLinks, ytDownloadsDir, ytAMVDir, ytAnShows, keyboardType, standardizeString

#from LinkAttribute import LinkAttribute
from bs4 import BeautifulSoup, SoupStrainer

import re

MAX_TRIES=3

AVAILABLE_SWITCHES=['v','h','s','m']

_VALID_URL = r"""^
				 (
					 (?:https?://)?                                       # http(s):// (optional)
					 (?:youtu\.be/|(?:\w+\.)?youtube(?:-nocookie)?\.com/|
						tube\.majestyc\.net/)                             # the various hostnames, with wildcard subdomains
					 (?:.*?\#/)?                                          # handle anchor (#/) redirect urls
					 (?!view_play_list|my_playlists|artist|playlist)      # ignore playlist URLs
					 (?:                                                  # the various things that can precede the ID:
						 (?:(?:v|embed|e)/)                               # v/ or embed/ or e/
						 |(?:                                             # or the v= param in all its forms
							 (?:watch(?:_popup)?(?:\.php)?)?              # preceding watch(_popup|.php) or nothing (like /?v=xxxx)
							 (?:\?|\#!?)                                  # the params delimiter ? or # or #!
							 (?:.*?&)?                                    # any other preceding param (like /?s=tuff&v=xxxx)
							 v=
						 )
					 )?                                                   # optional -> youtube.com/xxxx is OK
				 )?                                                       # all until now is optional -> you can pass the naked ID
				 ([0-9A-Za-z_-]+)                                         # here is it! the YouTube video ID
				 (?(1).+)?                                                # if we found the ID, everything can follow
				 $"""


				 
YOUTUBE_DL="C:\\Users\\Kevin\\Util\\youtubeDL.py "

def getPageSource(link):
	return openURL({}).open(link).read()

	
def sanitize_filename(s, restricted=False, is_id=False):
    """Sanitizes a string so it could be used as part of a filename.
    If restricted is set, use a stricter subset of allowed characters.
    Set is_id if this is not an arbitrary string, but an ID that should be kept if possible
    """
    def replace_insane(char):
        if char == '?' or ord(char) < 32 or ord(char) == 127:
            return ''
        elif char == '"':
            return '' if restricted else '\''
        elif char == ':':
            return '_-' if restricted else ' -'
        elif char in '\\/|*<>':
            return '_'
        if restricted and (char in '!&\'()[]{}$;`^,#' or char.isspace()):
            return '_'
        if restricted and ord(char) > 127:
            return '_'
        return char

    result = u''.join(map(replace_insane, s))
    if not is_id:
        while '__' in result:
            result = result.replace('__', '_')
        result = result.strip('_')
        # Common case of "Foreign band name - English song title"
        if restricted and result.startswith('-_'):
            result = result[2:]
        if not result:
            result = '_'
    return result

	
	
def extract_id(url):
	d=url.split(" ")
	url="".join(map(str,d))
	
	mobj = re.match(_VALID_URL, url, re.VERBOSE)
	
	if mobj is None:
		print(u'ERROR: invalid URL: %s' % url)
		video_id=None
		
	video_id = mobj.group(2)
	return video_id
	
def isEncodable(ytLink, titleHolder):

	result=True
	videoID=extract_id(ytLink)
	
	videoInfoURL = 'http://www.youtube.com/get_video_info?&video_id=%s&ps=default&eurl=&gl=US&hl=en'% (videoID)

	infoSource=openURL({}).open(videoInfoURL).read()
	
	title= infoSource[ infoSource.index("&title")+7: ]#cut from title to end
	title= title[ :title.index("&")]
	title= unquote_plus(title).decode('ascii','ignore')
	title=title.replace('/','').replace('&','').replace(':','').replace('+','').replace('*','')
	title=" ".join(title.split())#http://stackoverflow.com/questions/1546226/the-shortest-way-to-remove-multiple-spaces-in-a-string-in-python
	titleHolder.append(title)
	
	
	
	
	try:
		
		s1=infoSource[ infoSource.index('&title')+7 :]
		s2=s1[:s1.index('&')]
		s3=sanitize_filename(s2, restricted=True)
		s4="".join([unquote_plus(s3),".mp4"])
		
		try:
			str(s4)
			
			
		except UnicodeEncodeError:
			result=False
			
	
	except ValueError:
		result=None
		
	
	return result


def getTitleFromSys(ytVidLink):
	

	YOUTUBE_DL="C:\\Users\\Kevin\\Util\\youtubeDL.py "
	commandArgs="".join([ytVidLink , " -q -s --get-filename --extract-audio --restrict-filenames --output %(title)s_%(id)s.%(ext)s "])

	proc = subprocess.Popen([YOUTUBE_DL, commandArgs], stdout=subprocess.PIPE, shell=True)
	(title, err) = proc.communicate()
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


def downloadMusic(ytVidLink, targetDir):
	
	titleHolder=[]
	command="".join([YOUTUBE_DL, ytVidLink , " --quiet --restrict-filenames --no-mtime --no-overwrites --extract-audio --output \"",targetDir,"\\%(title)s_%(id)s.%(ext)s\""])
	title=getTitleFromSys(ytVidLink)
	title="".join([targetDir,"\\",title])
	"""
	if ( isEncodable(ytVidLink, titleHolder) ):
		#command="".join([YOUTUBE_DL, ytVidLink , " --quiet --no-mtime --no-overwrites --output \"",targetDir,"\\%(title)s.%(ext)s\""])
		
		#title="".join([targetDir,"\\",titleHolder[0],".mp4"])
		
		title="".join([targetDir,"\\",titleHolder[0],".m4a"])
		command="".join([YOUTUBE_DL, ytVidLink , " --quiet --no-mtime  --max-downloads 1 --no-overwrites --extract-audio --output \\\"",title,"\\\""])
		
		
		#extract audio was no longer working so we just now download the video and then convert to mp3 after
	else: #if ( isEncodable(ytVidLink)==True ) :
		#command="".join([YOUTUBE_DL, ytVidLink , " --quiet --restrict-filenames --no-mtime --no-overwrites --output \"",targetDir,"\\%(title)s_%(id)s.%(ext)s\""])
	
		
		#title="".join([targetDir,"\\",titleHolder[0],"_",extract_id(ytVidLink),".mp4"])
		
		title="".join([targetDir,"\\",titleHolder[0],"_",extract_id(ytVidLink),".m4a"])
		command="".join([YOUTUBE_DL, ytVidLink , " --quiet --restrict-filenames --no-mtime  --max-downloads 1 --no-overwrites --extract-audio --output \\\"",title,"\\\""])
		
	"""
		
	
	print command
	system(command)
	
	#conversion
	convertCommand="%UtilResources%/convertToMp3.py " + "\""+title+"\""
	print "Converting : ", title
	sleep(2)
	system(convertCommand)
	
	#Thread(target=system,args=(command,)).start()
	#sleep(3)
	
	
def downloadVideo(ytVidLink, targetDir):
	
	
	try:
		titleHolder=[]
		
		
		if ( isEncodable(ytVidLink,titleHolder) ) :
			command="".join([YOUTUBE_DL, ytVidLink , " --rate-limit 100m  --no-mtime --no-overwrites --output \"",targetDir,"\\%(title)s.%(ext)s\""])
		else:
			command="ECHO Video is restricted from downloads" 
			
		
		Thread(target=system,args=(command,)).start()
		sleep(3)
	
	except:
		pass
				
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
		vidLink=" ".join(map(str,argv[1:])).replace('\\','/')
		downloadMusic(vidLink,musicDir)
		
		
			
	
	else:#multiple music
		
		
		DEFAULT_LINKS=["http://www.reddit.com/r/dubstep","http://www.reddit.com/r/japanesemusic", "http://www.reddit.com/r/animemusic/","http://www.reddit.com/r/vocaloid"]
		#DEFAULT_LINKS=[r"""http://www.reddit.com/r/vocaloid"""]
		
		if(len(argv)>1):
			DEFAULT_LINKS=argv[1:]
		
		vidList=getVidList(DEFAULT_LINKS)
		
		
		
		for vidLink in vidList:
			if(vidLink is not None):
				#downloadMusic(vidLink,screeningDir)
				Thread(target=downloadMusic,args=(vidLink,screeningDir,)).start()
				sleep(3)
		
		
		
		
		
		
