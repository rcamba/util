from win32com import client
from mouseMacro import rightclick
from time import sleep
from os import system

if __name__ == "__main__":
	
	system (r""" "%userprofile%\\"Application Data"\\Microsoft\\"Internet Explorer"\\"Quick Launch"\\"Shows Desktop.lnk"" """)
	
	rightclick()
	shell=client.Dispatch("WScript.Shell")
	shell.SendKeys("vd")