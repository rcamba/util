from sys import argv
import subprocess

ytVidLink=argv[1]

YOUTUBE_DL="C:\\Users\\Kevin\\Util\\youtubeDL.py "
commandArgs="".join([ytVidLink , " -q -s -e --restrict-filenames "])

proc = subprocess.Popen([YOUTUBE_DL, commandArgs], stdout=subprocess.PIPE, shell=True)
(out, err) = proc.communicate()
print out



