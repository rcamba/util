from sys import argv
from os import system
from time import sleep

timeLeft=int(argv[1])

argv=argv[2:]
argv= " ".join(map(str, argv))


while(timeLeft>0):
	print "Time remaining: ", timeLeft
	sleep(60)
	timeLeft=int(timeLeft)-1

system(argv)