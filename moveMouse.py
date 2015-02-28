from root import moveMouse
from sys import argv, path
from os import getenv
path.insert(0, getenv("UtilResources"))
from mouseMacro import getpos
g=getpos()
moveMouse(int(g[0]+int(argv[1])),int(g[1]+int(argv[2])))