def getFolderSize(folderPath):
	from win32com import client
	from os import path
	
	if path.isdir(folderPath):
		
		fso = client.Dispatch("Scripting.FileSystemObject")
		folder = fso.GetFolder(folderPath)
		MB=1024*1024.0
		print  "%.2f MB"%(folder.Size/MB)
	
	else:
		print folderPath, " is not a valid or accessible directory."
		

if __name__ == "__main__":
	from sys import argv
	from os import getcwd
	
	if(len(argv)==2):
		getFolderSize(argv[1])
	else:
		getFolderSize(getcwd())
	
	
