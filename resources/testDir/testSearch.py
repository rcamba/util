from os import path, listdir
from root import standardizeString, switchBoard, printNumberedList, chooseFromNumberedList, setClipboardData, compareLists
from sys import argv
#search for file- implement clipboard selection
# let , equal to or

# SO BROKEN, FIX IT PLS
# a1 b1 :finds items that contain a1 AND b1
# a1,b1 :finds items that contain a1 or b1
#c1 a1,b1 :finds items that contain c1 AND (a1 or b1)

AVAILABLE_SWITCHES=['l','s']
messagedAlready=False

def preHandleSearchTargetList(searchTargetList):
	finalPossRes=[]
	zList=[]
	
	for i in range(len(searchTargetList)-1,-1,-1):
		sTarg=searchTargetList[i]
		if ',' in sTarg:
			zList.extend(sTarg.split(','))
			searchTargetList.remove(sTarg)
	
	
	
	if len(zList)==0:
		return compareLists(findFile(searchTargetList), findFile(zList), similar=False)
	else:
		pass
	"""
	finalPossRes=[]
	zList=[]
	for i in range(len(searchTargetList)-1,-1,-1):
		sTarg=searchTargetList[i]
		if ',' in sTarg:
			zList.extend(sTarg.split(','))
			searchTargetList.remove(sTarg)
	
	for z in zList:
		for searchTarg in searchTargetList:
			finalPossRes.extend(findFile( [z,searchTarg] ))
	else:
			for searchTarg in searchTargetList:
				finalPossRes.extend(findFile( [searchTarg] ))
	
	return list(set(finalPossRes))
	"""
	
def findFile(searchTargetList):  #"Implement selected directories ?"
	
	possibleResults=[]
	
	for file in fileList:
		counter=0
		for searchTarget in searchTargetList:
			if standardizeString(searchTarget) in standardizeString(path.split(file)[1]):
				counter=counter+1
				
			if counter==len(searchTargetList):
				possibleResults.append("\""+file+"\"")
			
			
	return possibleResults
	
def errMsgHandler():
	global messagedAlready
	if (messagedAlready==False):
		print "Access to some folders have been denied. Run again with '-l' parameter to view the folder log"
		messagedAlready=True
	
def collectAllFiles(directory):
	#os.access(r'C:\haveaccess', os.R_OK)
	fileList=[]
	

	try:
		fileList=listdir(directory)
	
	except WindowsError as err:
		
		if  err.errno==13:	
			if 'l' in switches:
				print "Access to ", err.filename, "is denied. Unable to search within this folder."
			else:
				errMsgHandler()
			
	
	
	
	

	
		
	
	
	for i in range(len(fileList)-1,-1,-1):
		file= fileList[i]
		fullFilePath= directory+"\\"+file
		
		
		if path.isdir(fullFilePath):	
			fileList.extend(collectAllFiles(fullFilePath))
		else:
			fileList.append(fullFilePath)# add only fullFilePath of files and not directories
			
		fileList.remove(file)
		
			
	return fileList
			

	
if __name__ == "__main__":
	
	switches=switchBoard(argv, AVAILABLE_SWITCHES)
	
	
	if len(argv)>2 :
		if  path.isdir(argv[1]):
		
			topDir=argv[1]
			searchTargetList=argv[2:]
			fileList=collectAllFiles(topDir)
			
			resultList=preHandleSearchTargetList(searchTargetList)
			#resultList=findFile(searchTarget)
			
			printNumberedList(resultList)
			if 's' in switches:
				uSelect=chooseFromNumberedList(resultList)
				setClipboardData(uSelect)
				
			
	else:
		print "Missing arguments. Usage find [directory][searchTarget1]...[searchTarget2]"
		
	
	
	