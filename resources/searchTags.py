"""
*Not using .bat because it reads commas as a separator/delimiter
"""
from sys import argv, stdin, stdout
from root import switchParser, printList, setClipboardData, chooseFromList, pipedList
from tag import getFilenameList, getTagList, getMixedFilenameList
from string import strip
from fnmatch import translate
import re


AVAILABLE_SWITCHES=['s','f','r']

def main(argList):
	if 'f' in switches:

		tagList=getTagList(argList[0])
		print tagList

	elif 'r' in switches:
		res=[]
		tList=getTagList()

		#res.extend([tag for tag in tList if arg in tag])
		pattern=translate(argList[0])
		reObj=re.compile(pattern)
		for tag in tList:
			match=reObj.findall(tag)
			if len(match)>0:
				res.append(tag)
		print res

		if len(res)==1:
			fList=map(lambda x: "\""+x+"\"", getMixedFilenameList(res))
			printList(fList)
			print res

		else:
			chooseFromTags(res)


	else:
		tagList= " ".join(map(str, argList)).split(',')
		tagList=map(strip,tagList)


		fileList=map(lambda x: "\""+x+"\"", getFilenameList(tagList))

		if 's' in switches:
			if len(switches['s'])>0:
				choice=fileList[int (switches['s'])-1]

			else:
				printList( fileList, pressToContinue=stdout.isatty() )

				if len(fileList)==1:
					choice=fileList[0]

				else:
					choice=chooseFromList(fileList)

			print choice
			setClipboardData(choice)

		else:
			printList( fileList, pressToContinue=stdout.isatty() )


def chooseFromTags(tList):
	printList(tList)
	choice=chooseFromList( tList )
	cfList=  getFilenameList(choice)
	printList(cfList)
	choice=chooseFromList( cfList)
	setClipboardData ( choice)

if __name__=="__main__":
	switches=switchParser(argv)


	if stdin.isatty()==False:#for using with nf/search
		print "Piped search"
		argList=pipedList( "".join(map(str,stdin.readlines())) )
		main(argList)

	elif len(argv)>1:
		main(argv[1:])


	else:

		tList=getTagList()
		tList.sort()
		chooseFromTags(tList)
