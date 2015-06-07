from win32gui import GetWindowText, IsWindowEnabled, EnumWindows
from win32process import GetWindowThreadProcessId
from psutil import Process, get_pid_list
from root import vlcTitleFile, setClipboardData, standardizeString, chooseFromList, printList
from os import listdir, path


def get_hwnds_for_pid (pid):
	def callback (hwnd, hwnds):

		if (IsWindowEnabled (hwnd)):
			_, found_pid = GetWindowThreadProcessId(hwnd)

			if found_pid == pid:
				hwnds.append (hwnd)

		return True

	hwnds = []
	EnumWindows (callback, hwnds)

	return hwnds

def get_VLC_Title():
	vlc_PID=-1
	vlcTitle=-1

	f=open(vlcTitleFile,"r")
	vlcNumFromFile=f.read()
	f.close()

	if(vlcNumFromFile.isdigit() and "media player" in GetWindowText( int(vlcNumFromFile) )):
		vlcHwnd=int(vlcNumFromFile)

		vlcTitle=titleFromHwnd(vlcHwnd)

	else:
		pidList=get_pid_list()
		for i in range(0,len(pidList)):
			process=Process(pidList[i])
			if(process.name=="vlc.exe"):
				vlc_PID=process.pid
				break;

		hwndList=get_hwnds_for_pid(vlc_PID)

		for i in range(0,len(hwndList)):
			if("media player" in GetWindowText (hwndList[i])):
				#print "-",
				vlcTitle=titleFromHwnd(hwndList[i])

				f=open(vlcTitleFile,"w+")
				f.write(str(hwndList[i]))
				f.close()

				break;

	return vlcTitle

def titleFromHwnd(vlcHwnd):
	return GetWindowText(vlcHwnd).replace("- VLC media player","")

def listAllFiles(fDir):

	fList=[]
	tempList = listdir(fDir)

	for file in tempList:
		file="".join([fDir,"\\",file])

		if path.isdir(file)==False:
			fList.append(file)
		else:
			fList.extend(listAllFiles(file))

	return fList

def searchMusicFileList(musicFileList, targetFile):

	resultsList=[]
	targetFile=standardizeString(targetFile)
	resultsList=[musicFile for musicFile in musicFileList if targetFile in standardizeString(musicFile) ]

	return resultsList


def findFilePath(vlcTitle):
	resultsList=[]
	topLevel="C:\\Users\\Kevin\\Music"
	musicFileList=listAllFiles(topLevel)
	if(type(vlcTitle)==str):
		resultsList=searchMusicFileList(musicFileList,vlcTitle)

		if(len(resultsList)>1):
			print "More than one result found"
			printList(resultsList)
			vlcTitle=chooseFromList(resultsList)

		elif(len(resultsList)==1):
			vlcTitle=resultsList[0]

		else:
			print "No results found"

		filePath="".join(['\"',standardizeString(vlcTitle),'\"'])
	else:
		print "VLC.exe process not found"

	return filePath




if __name__ == "__main__":

	vlcTitle=get_VLC_Title()

	print "+ Currently playing:"
	printList([vlcTitle], aes="none")
	fp=findFilePath(vlcTitle)
	setClipboardData(fp)
	printList([fp], aes="none")






