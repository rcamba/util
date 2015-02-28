from os import system, getpid
from time import sleep

from root import resizeWindow, moveWindow, getClipboardData, sVLC_PID
from mouseMacro import getpos, move
from get_VLC_Title import get_VLC_Title, setFilePathToClipboard
from tag import getTagList

windowWidth=950
windowHeight=150

resizeWindow(windowWidth,windowHeight,"",getpid())
#moveWindow( (1920/2)-(windowWidth/2), (1080/2)-(windowHeight/2), "", getpid())
if getpos()[0]>1920:
	moveWindow( int(3840*0.75)-(windowWidth/2), getpos()[1]-200, "", getpid())
	
else:
	moveWindow( (1920/2)-(windowWidth/2), getpos()[1]-200, "", getpid())




vlcTitle=get_VLC_Title()
setFilePathToClipboard(vlcTitle)

print  vlcTitle
print getTagList(getClipboardData().replace("\"",""))


sleep(2)
