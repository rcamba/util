from os import listdir, path
from sys import argv
from root import compareLists, switchBoard, printNumberedList
AVAILABLE_SWITCHES=['c']
def findAllFolders(dir):
	
	fList= listdir( dir ) 
	
	for i in range(len( fList)-1,-1,-1 ):
		
		if path.isdir( dir+"/"+fList[i] )==False:
			fList.remove(  fList[i] )
	
	return fList
	
def compareFolders(f1, f2):
	printNumberedList(  compareLists( f1, f2, False) )
	
def compareContents(dir1, dir2):
	if dir1==dir2:
		return True
	else:
		return dir2
		
def pushCC(dirList1,dirList2,newFileList):

	
	dirList1.sort()
	dirList2.sort()
	j=0
	for i in range(0, min( len(dirList1), len(dirList2) ) ) :
		
		res=compareContents(dirList1[i], dirList2[j])
		if(res!=True):
			newFileList.append(res)
		else:
			j=j+1
			newDir1=findAllFolders(dirList1[i]  )
			newDir2=findAllFolders(dirList2[j]  )
			print newDir1
			print newDir2
			pushCC(newDir1, newDir2,newFileList)
		
		j=j+1
	
if __name__ == "__main__":
	switches=switchBoard(argv)
		
	if 'c' in switches:#compare contents of folder, if contents differ, print folders
		
		dirList1=findAllFolders(argv[1].replace("\\","/"))
		dirList2=findAllFolders(argv[2].replace("\\","/"))
		newFileList=[]
		pushCC(dirList1,dirList2, newFileList)
		
		printNumberedLIst(newFileList)
	
	else:
		dirList1=findAllFolders(argv[1].replace("\\","/"))
		dirList2=findAllFolders(argv[2].replace("\\","/"))
		
		compareFolders(dirList1, dirList2)
		
