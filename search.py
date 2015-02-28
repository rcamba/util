def getStringArgs(argList, switchCarrier):
	resultStr=""
	switchString=""
	
	for i in range(1,len(argList)):
		
		if("-" not in argList[i][0]):
			resultStr="".join([resultStr.strip()," ",argList[i]])
			
		else:
			switchString="".join([switchString," ",argList[i]])
			switchString=switchString.strip()
	
	if('-f' in argList and len(resultStr)>0):		
		resultStr="".join(["\"",resultStr.strip(),"\""])
		
	switchCarrier.append(switchString)
	
	
	return resultStr


	
if __name__ == "__main__":
	from sys import argv
	from os import system
	
	switchCarrier=[]
	
	stringArgs=getStringArgs(argv, switchCarrier)	
	switchString=switchCarrier[0]
	
	if(len(stringArgs)>0):
		stringArgs="".join([stringArgs.strip()," ",switchString])
	else:	
		stringArgs=switchString
	
	
	system("".join(["%UtilResources%/searchTags.pyc ", stringArgs]))
	
	