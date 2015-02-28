from sys import argv
from os import system
	
if __name__ == "__main__":
	stringArgs=" ".join(map(str,argv[1:]))
	system("".join(["%UtilResources%/toDoList.pyc -a ", stringArgs]))