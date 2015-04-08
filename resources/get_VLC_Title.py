from win32gui import GetWindowText, IsWindowEnabled, EnumWindows
from win32process import GetWindowThreadProcessId 
from psutil import Process, get_pid_list
from root import vlcTitleFile, printNumberedList, setClipboardData, standardizeString, chooseFromNumberedList, cen, fileSearch
from os import listdir, path
from threading import Thread


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
				print "-",
				vlcTitle=titleFromHwnd(hwndList[i])
				
				f=open(vlcTitleFile,"w")
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
	for musicFile in musicFileList:
		if targetFile in standardizeString(musicFile):
			resultsList.append(musicFile)
			
	return resultsList
	
def setFilePathToClipboard(vlcTitle):
	
	resultsList=[]
	topLevel="C:\\Users\\Kevin\\Music"
	musicFileList=listAllFiles(topLevel)
	
	if(type(vlcTitle)==str):
		
		#resultsList=fileSearch(vlcTitle)
		resultsList=searchMusicFileList(musicFileList,vlcTitle)
		
		#store vlc file name in vlcTitle after printing
		
		if(len(resultsList)>1):
			print "More than one result found"
			printNumberedList(resultsList)
			#vlcTitle=resultsList[int(chooseFromNumberedList(resultsList))]
			vlcTitle=chooseFromNumberedList(resultsList)
		elif(len(resultsList)==1):
			vlcTitle=resultsList[0]
			#cen()
		else:
			print "No results found"
	
		
		
		setClipboardData("".join(['\"',standardizeString(vlcTitle),'\"']))
	else:
		print "VLC.exe process not found"
	#file=open(vlcTitleFile,"w")
	#file.write("".join(["\"",vlcTitle,"\""]))
	#file.close()


	
	

if __name__ == "__main__":
	
	vlcTitle=get_VLC_Title()
	print "+ Currently playing: ", vlcTitle
	Thread(target=setFilePathToClipboard, args=(vlcTitle,)).start()
	
	


	
	