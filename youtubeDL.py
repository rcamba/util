from os import system
from sys import argv 

if __name__ == "__main__":	

	argString=" ".join(map(str,argv[1:]))
	system( "".join( ["C:\Users\Kevin\Downloads\youtube-dl.exe ",argString] ) )
	
	
	
	#system( "".join( ["C:\Users\Kevin\Downloads\youtube-dl-2013.02.25.tar\youtube-dl-2013.02.25\youtube-dl\youtube_dl\__main__.py ",argString] ) )
	
 