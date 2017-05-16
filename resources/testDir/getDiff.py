
alt:
	emulate vcs?


from sys import argv,path
from os import getenv


path.insert(0,getenv("UtilResources"))
from root import set_console_color, get_console_color
def printDifference(newest, older):
	f1=open(newest).read().split('\n')
	f2=open(older).read().split('\n')

	if len(f1) > len(f2):
		limit=len(f1)
		smaller=f2
		larger=f1
	else:
		limit=len(f2)
		smaller=f1
		larger=f2

	set_console_color("red")

	for i in range(0,limit):

		if len(smaller[i])>0 or len(larger[i])>0:
			if i > len(smaller):
				print "Line ", i+1,": ",larger[i]
			elif smaller[i]!=larger[i]:

				print "Line ", i+1,": ", f2[i]#print what's different in the older file

	set_console_color(origColor)

if __name__=="__main__":
	"""
	Compare newest version with older version
	print differences in red
	"""
	origColor=get_console_color()
	if (len(argv)>2):
		printDifference(argv[1], argv[2])
	else:
		print "Missing arguments"