from os import system
from sys import argv

argv=argv[1:]
argStr=" ".join(map(str,argv))
system("\"C:\\Program Files (x86)\\VideoLAN\\VLC\\vlc.exe\" " + argStr )
