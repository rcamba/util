
from string import rstrip

def findTag(line):
	tag=""
	for c in line:
		if c!='\"':
			tag=tag+c
		else:
			break
	return tag[:-1]

reader=open("tagFile.txt")
lineList=map(rstrip,reader.readlines())
reader.close()

writer=open("tagFile.txt",'w')

for line in lineList:
	tag=findTag(line)
	
	rest=line[ line.index('\"'):]
	
	writer.write(tag+"::")
	writer.write(rest+",")
	writer.write("\n")
	
writer.close()
	
	