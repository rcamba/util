from tag import removeTags, getTagList,getFilenameList
from sys import argv
from root import printList, switchParser, keyPressInput
AVAILABLE_SWITCHES=['f','t']
	
def _chooseFromList(aList):
	choiceList=[]
	if len(aList)>1:
		print "Enter number(s) separated by commas"
		
		try:
			input= raw_input()
		except EOFError:#pipes
			input=keyPressInput()
				
		choices=input.split(',')
		choices=map(int,choices)
		
		for choice in choices:
			choiceList.append( aList[choice-1] )
	
	else:
		choiceList.append( aList[0] )
		
	return choiceList
	
def untagUsingTag(tag):
	fList=getFilenameList( tag )
	if len(fList)>0:
		printList(fList)
		choiceList=_chooseFromList(fList)
		for choiceFile in choiceList:
			removeTags([tag], choiceFile)

def untagUsingFilename(filename):
	tagList=getTagList(filename)
	if len(tagList)>0:
		printList(tagList)
		choiceList=_chooseFromList(tagList)
		for choiceTag in choiceList:
			removeTags([choiceTag], filename)

if __name__ == "__main__":
	switches=switchParser(argv, AVAILABLE_SWITCHES)
	
	if len(argv)>1 and ('t' in switches or 'f' in switches):
		
		if 't' in switches :
			tag=argv[1].strip()
			untagUsingTag(tag)
			
			
			
		elif 'f' in switches:
			filename=argv[1].strip()
			untagUsingFilename(filename)
			
	else:
		print "Invalid parameters"
		print "Usage untag[-f filename][-t tag]"
	
	