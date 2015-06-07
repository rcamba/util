from sys import argv
from os import listdir,path, system
from root import screeningDir


def convertToMp3(mp4File):
	if "\"" not in mp4File:
		mp4File= "\""+ mp4File+"\""
	command="ffmpeg -y -loglevel panic -i "+mp4File +" -f mp3 -ab 192000 -vn "+ mp4File.replace(".mp4", ".mp3").replace(".m4a", ".mp3")
	print command
	system(command)
	system("del " + mp4File)
def getMp4List(givenDir):
	mp4List=listdir(givenDir)
	for i in range(len(mp4List)-1,-1,-1):
		if( path.splitext(mp4List[i])[1]==".mp4" or path.splitext(mp4List[i])[1]==".m4a"):
			mp4List[i]="\""+givenDir+"\\"+mp4List[i]+"\""
		else:
			mp4List.remove(mp4List[i])

	return mp4List
if __name__ == "__main__":

	if len(argv) >1:
		convertToMp3(argv[1])
	else:
		mp4List=getMp4List(screeningDir)
		for mp4File in mp4List:
			convertToMp3(mp4File)