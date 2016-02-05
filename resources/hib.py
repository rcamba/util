from sys import stdout, argv
from time import sleep, time, strftime, localtime
from root import hibLog, errorAlert
from toDoList import viewToDoList
from datetime import datetime
from ctypes import windll
from os import system


def loadingSplash(timeLimit, output="", splash=['', '.', "..", "..."]):

	def backspaceStdout(string):
		result = ""
		for i in range(0,len(string)):
			result += "\b"
		stdout.write(result)

	def clearStdOut(string):
		clear =""
		for i in range(0,len(string)):
			clear = clear + " "
		stdout.write(clear)

		return clear

	i = 0
	stdout.write(output)
	startTime = time()
	while (time()-startTime) < timeLimit :

		splashText = splash[i]
		stdout.write(splashText)
		sleep(1)
		stdout.flush()

		backspaceStdout(splashText)

		i += 1
		if i == len(splash):
			backspaceStdout(clearStdOut(splashText))
			i = 0

	stdout.flush()
	backspaceStdout(output)


def createLog():
	"""Opens hibLog and appends date and time to the file"""

	f = open(hibLog, 'a')
	t = localtime()
	s = " ".join([str(strftime("%B/%d/%Y\t %H:%M", t)), '\n'])
	f.write(s)
	f.close()


def hibernate():

	"""
	hib_cmd = r"C:\Windows\System32\rundll32.exe " +
	"PowrProf.dll,SetSuspendState"
	"""

	hib_cmd = "shutdown /h"
	system(hib_cmd)
	viewToDoList()


def main(timeLimit):
	"""
	Sets program to sleep for timeLimit minutes
	Hibernate log is created after sleep with time stamp
	Calls toDoList to be viewable when resuming from hibernation
	Sets the computer to hibernate
	"""

	for i in range(int(timeLimit), 0, -1):
		output = "Time remaining until hibernation: {}".format(str( i))
		loadingSplash(60, output)

	createLog()
	hibernate()


if __name__ == "__main__":

	#windll.kernel32.SetConsoleCtrlHandler(0, 1)  # disables sigint / ctrl + c

	if(len(argv) < 2):
		errorAlert("Missing time parameter")

	else:
		try:
			main(int(argv[1]))

		except ValueError:
			errorAlert("Argument must be an integer")