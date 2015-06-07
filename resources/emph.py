"""[emph]asize"""

from sys import argv
from root import setClipboardData
from string import upper


if __name__ == "__main__":
	if len(argv)>1:
		argString=" ".join(map(str,argv[1:]))
		setClipboardData(argString.upper())

	else:
		print "Missing emphasis argument. \nUsage emph [text]"