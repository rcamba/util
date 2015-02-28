from os import getenv
from sys import path as sysPath

sysPath.insert(0,getenv("UtilResources"))
from cmdCursorPos import centerCMD
from mouseMacro import rightclick

if __name__=="__main__":
	centerCMD()
	rightclick()