from time import sleep
from string import lower
from os import system, listdir, path
from threading import Thread
from bs4 import BeautifulSoup
from sys import argv
from cleanFileNames import cleanString
from urllib2 import quote
from subprocess import Popen
from random import randint

from root import screeningDir, musicDir, switchBoard, getAllPageLinks, yt_dls_dir, yt_amv_dir, outputFromCommand, errorAlert, deletedScreenedLog



"""
 -m single music
 -v multiple video
 -s single video
"""

MAX_TRIES=3
AVAILABLE_SWITCHES=['v','h','s','m']

YT_DL_PROG = "C:\\Users\\Kevin\\Downloads\\youtube-dl.exe"

def rand_sleep():
	sleep(randint(1,3))


def get_dry_title(vid_link):

	yt_dl_opts = "-q -s --get-filename --extract-audio --restrict-filenames --output ".split()
	output_format = "%(title)s_%(id)s.%(ext)s"
	title_cmd = [YT_DL_PROG, vid_link] + yt_dl_opts + [output_format]
	title = outputFromCommand(title_cmd)
	return title


def get_vid_list(links_list):

	vid_list = []
	for link in links_list:

		print "Retrieving video list from: ", link

		i = 0
		page_links = getAllPageLinks(link)

		while len(page_links) <= 1 and i < MAX_TRIES:
			page_links = getAllPageLinks(link)
			i += 1
			print "Retry # ", i
			rand_sleep()

		if len(page_links) > 1:
			vid_list.extend(parse_yt_links(page_links))

	return vid_list


def parse_yt_links(page_links):

	v_ID_list = []
	for i in range(len(page_links) - 1, -1, -1):

		page_links[i] = page_links[i].get("href")
		if page_links[i] is not None:

			if "youtube" not in page_links[i]:
				page_links[i] = "youtube.com" + page_links[i]

			if "http" not in page_links[i] :
				page_links[i] = "http://" + page_links[i]

			try:
				base_url = page_links[i][:page_links[i].index("watch?") + 6]
				v_ID = page_links[i][page_links[i].index("v="):]
				page_links[i] = base_url + v_ID

				# try and slice off '&' options in the link
				# e.g: watch?v=IDHERE&list=PLAYLIST
				# slices off "&list=PLAYLIST"
				if page_links[i].find('&') > -1:
					page_links[i] = page_links[i][:page_links[i].index('&')]

				# prevent duplicates
				if v_ID	 not in v_ID_list:
					v_ID_list.append(v_ID)
					page_links.remove(page_links[i])

			except (ValueError, IndexError):
				page_links.remove(page_links[i])

	return page_links


def alreadyDownloaded(title, targDir):
	retVal=False
	fList= listdir(targDir)
	t=path.splitext(title)[0].lower()
	for f in fList:

		if t==path.splitext(f)[0].lower():
			retVal=True
			break

	return retVal

def downloadMusic(vid_link, target_dir):

	command="".join([YT_DL_PROG, vid_link , " --quiet --restrict-filenames --no-mtime --no-overwrites --extract-audio --output \"",target_dir,"\\%(title)s_%(id)s.%(ext)s\""])
	title=get_dry_title(vid_link)
	if len(title)>0:

		title=cleanString(title)
		if alreadyDownloaded(title, musicDir)==False:#check musicDir instead of screening dir since there's no overwrites anyway
			if path.splitext(title.lower())[0] not in deletedMusicList:
				print "Downloading:", title
				title="".join([target_dir,"\\",title])

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
		errorAlert( "Empty title for " + vid_link)

def dl_single_video(vid_link, target_dir):

	yt_dl_opts = "--quiet --rate-limit 100m  --no-mtime --no-overwrites --output".split()
	YT_DL_OUTPUT_FILE = "{targDir}\\%(title)s_%(id)s.%(ext)s".format(targDir=target_dir)

	dl_vid_cmd = [YT_DL_PROG, vid_link] + yt_dl_opts + [YT_DL_OUTPUT_FILE]

	title = get_dry_title(vid_link)
	print "Downloading:", title

	proc = Popen(dl_vid_cmd)


def dl_multi_video(vid_link="http://www.reddit.com/r/amv"):

	print "Downloading multiple videos from {}".format(vid_link)

	vid_list = get_vid_list([vid_link])

	for vid in vid_list:
		if vid is not None:
			dl_single_video(vid, yt_amv_dir)


if __name__ == "__main__":

	vid_list=[]

	char_func_mapping = {
		's': lambda: dl_single_video(vid_link, yt_dls_dir),
		'v': lambda: dl_multi_video(vid_link) if len(vid_link) > 0 else dl_multi_video(),
		'm': lambda: dl_single_song(),
		'': lambda: dl_multi_song()
	}

	opt = argv[1].replace('-', '')
	vid_link = ""
	if len(argv) > 2:
		vid_link = quote(argv[2], safe="%/:=&?~#+!$,;'@()*[]")

	char_func_mapping[opt]()

	"""
	if 's' in switchList:  # single video
		print "Dowloading single video"
		vid_link=" ".join(map(str,argv[1:])).replace('\\','/')
		downloadVideo(vid_link,yt_dls_dir)

	elif 'v' in switchList:#multiple video
		print "Downloading multiple videos from source"
		DEFAULT_LINKS=["http://www.reddit.com/r/amv"]

		if(len(argv)>1):
			DEFAULT_LINKS=argv[1:]

		vid_list=get_vid_list(DEFAULT_LINKS)

		for vid_link in vid_list:
			if(vid_link is not None):
				downloadVideo(vid_link,yt_amv_dir)


	elif 'm' in switchList:#single music
		print "Downloading single music"
		deletedMusicList=open(deletedScreenedLog).read().split("\n")
		vid_link=" ".join(map(str,argv[1:])).replace('\\','/')
		downloadMusic(vid_link,musicDir)

	else:#multiple music

		DEFAULT_LINKS=["http://www.reddit.com/r/japanesemusic", "http://www.reddit.com/r/animemusic/","http://www.reddit.com/r/vocaloid"]

		if(len(argv)>1):
			DEFAULT_LINKS=argv[1:]

		vid_list=get_vid_list(DEFAULT_LINKS)
		deletedMusicList=open(deletedScreenedLog).read().split("\n")

		for vid_link in vid_list:
			if(vid_link is not None):
				#downloadMusic(vid_link,screeningDir)
				Thread(target=downloadMusic,args=(vid_link,screeningDir,)).start()
				sleep(3)
	"""