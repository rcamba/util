"""
*Not using .bat because it reads commas as a separator/delimiter
"""
from sys import argv, stdin, stdout
from root import switchParser, printList, setClipboardData, chooseFromList, pipedList
from tag import getFilenameList, getTagList, handleTagSwitch
from string import strip


AVAILABLE_SWITCHES=['s','f','r']

def main(argList):
	switches = switchParser(argList)

	if 'f' in switches:
		file = argList[0]
		tagList=getTagList(file)
		print tagList

	elif 'r' in switches:
		res=handleTagSwitch("r", argList=argList)
		if len(res)==1:
			fList=map(lambda x: "\""+x+"\"", getFilenameList(res))
			printList(fList)
			print res

		elif len(res)>0:
			chooseFromTags(res)


	else:
		tags = map(lambda xStr: xStr.replace(',', ''), argList)

		fileList=map(lambda x: "\""+x+"\"", getFilenameList(tags))

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
			if len(fileList)>0:
				choice = fileList[len(fileList)-1]
				setClipboardData(choice)
			printList( fileList, pressToContinue=stdout.isatty() )


def chooseFromTags(tList):
	printList(tList)
	choice=chooseFromList( tList )
	cfList=  getFilenameList(choice)
	printList(cfList)
	choice=chooseFromList( cfList)
	setClipboardData ( choice)

if __name__=="__main__":


	if stdin.isatty() is False:#for using with nf/search
		print "Piped search"
		argList = pipedList("".join(map(str, stdin.readlines())))
		main(argList)

	elif len(argv) > 1:
		main(argv[1:])

	else:

		tList=getTagList()
		tList.sort()
		chooseFromTags(tList)
