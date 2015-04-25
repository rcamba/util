from tag import removeTags, getTagList,getFilenameList
from sys import argv
from root import printList, switchParser, chooseFromList
AVAILABLE_SWITCHES=['f','t']
	
def untagUsingTag(tag):
	fList=getFilenameList( tag )
	if len(fList)>0:
		printList(fList)
		choiceFile=chooseFromList(fList)
		removeTags([tag], choiceFile)

def untagUsingFilename(filename):
	tagList=getTagList(filename)
	if len(tagList)>0:
		printList(tagList)
		choiceTag=chooseFromList(tagList)
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
	
	