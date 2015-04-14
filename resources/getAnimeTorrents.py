#GAT:

from root import getAllPageLinks, downloadedTorFiles, printNumberedList, downloadTorBackLog
import re
import datetime
import os
import time
import operator 
class TorrentDownload:
	def __init__(self,newPattern,newFansub_ID,newSearchTerms,newOption=""):
		self.pattern=newPattern
		self.fansub_ID=newFansub_ID
		self.searchTerms=newSearchTerms.replace(' ','+')
		
		self.pattern=self.pattern.replace(' ','.+')
		self.pattern='.+'+self.pattern+'.+'
		
		if(len(newOption)>0):
			self.option=newOption
		else:
			self.option=None
			
		
		self.pageLinkList=[]
			
	def getPattern(self):
		return self.pattern
		
	def getFansubID(self):
		return str(self.fansub_ID)
		
	def getSearchTerms(self):
		return self.searchTerms
		
	def getOptions(self):
		return self.option
		
	
		
	def __str__( self ):
		if self.option!=None:
			return ", ".join([str(self.pattern), str(self.fansub_ID), str(self.searchTerms), str(self.option)])
		else:
			return ", ".join([str(self.pattern), str(self.fansub_ID), str(self.searchTerms)])

class TorLog:
	def __init__(self, newDate, newFileName):
		self.date=newDate
		self.filename=newFileName
		
def prepareForDownload():
	pass
			
def isPatternInTorList(pattern, torList):
	result=False
	
	for tor in torList:
		
		if tor.getPattern()==pattern:
			result=True
			break
			
	return result
	
def castBackLogToTorObj(token):
	if len(token)==3:
		return ( TorrentDownload(token[0], token[1], token[2]) )
	elif len(token)==4:
		return ( TorrentDownload(token[0], token[1], token[2], token[3]))
	
def addBackLogToTorList(torList):
	backLogList=open(downloadTorBackLog).read().split("\n")
	
	if len(backLogList)>0:
		
		for tor in backLogList:
			if(len(tor))>0:
				token=tor.split(',')
				pattern= token[0]
				if isPatternInTorList(pattern, torList)==False:
					generatedTorObj=castBackLogToTorObj(token)
					print "Added back logged torrents:", pattern
					torList.append(generatedTorObj)
	
	#clear backlog file
	f=open(downloadTorBackLog,'w')
	f.close()

def downloadedThisWeek(tor, torLog):
	pass
	"""
	for p in tor.pageLinkList:
		print p.text
	torLog=torLog[-50:]
	(today - timedelta(days=today.weekday())).strftime(TIME_FORMAT)#last monday
	(today + timedelta(days=-today.weekday()-1, weeks=1)).strftime(TIME_FORMAT)#coming sunday
	#for p in tor.pageLinkList:
		#for log in torLog:
			#print p.text in log.filename
	
	"""
def getTorListFromDay(day):
	
	torList=[]
	
	HORRIBLESUBS_ID=64513
	COMMIE_ID=76430
	UNDERWATER_ID=265
	DAMEDESUYO_ID=227008
	FFF_ID=73859
	if day=="Tuesday": 
		torList.append( 
			TorrentDownload("Nisekoi", COMMIE_ID, "Nisekoi 2")
		)
		
		torList.append( 
			TorrentDownload("Naruto 720", HORRIBLESUBS_ID, "Naruto Shippuuden", "LatestOnly")
		)
		
	elif day=="Wednesday":
		torList.append( 
			TorrentDownload("\[HorribleSubs\] Shinmai Maou no Testament - \d+ \[720p\].mkv", HORRIBLESUBS_ID, "Shinmai Testament")
		)
		
		
		
		
		
	elif day=="Thursday":
		torList.append( 
			TorrentDownload("\[HorribleSubs\] Saekano - \d+ \[720p\].mkv", HORRIBLESUBS_ID, "Saekano")
		)
		
		torList.append( 
			TorrentDownload("\[HorribleSubs\] Naruto Shippuuden - \d+ \[720p\].mkv", HORRIBLESUBS_ID, "Naruto Shippuuden", "LatestOnly")
		)
		
		
		
	
	
		
		torList.append( 
			TorrentDownload("\[Commie\] Kantai Collection - \d+ \[\w+\].mkv", COMMIE_ID, "Kantai")
		)
		
		
	elif day=="Friday":
		
		
		
		
		torList.append( 
			TorrentDownload("\[HorribleSubs\] Kuroko's Basketball 3 - \d+ \[720p\].mkv", HORRIBLESUBS_ID, "Kuroko")
		)
			
	
		torList.append( 
			TorrentDownload("\[Commie\] Aldnoah.Zero - \d+ \[\w+\].mkv", COMMIE_ID, "Aldnoah")	
		)
		
		torList.append( 
			TorrentDownload("\[Commie\] Shigatsu wa Kimi no Uso - \d+ \[\w+\].mkv", COMMIE_ID, "Shigatsu")	
		)
		
		
		

	addBackLogToTorList(torList)
		
			
	return torList
			
def addLinksAndText(torrentDownloadObject):
	
	pattern=torrentDownloadObject.getPattern()
	searchUser=torrentDownloadObject.getFansubID()
	searchTerm=torrentDownloadObject.getSearchTerms()
	searchLink="http://www.nyaa.se/?page=search&cats=0_0&filter=0&term="+searchTerm+"&user="+ searchUser
	print searchLink
	resultList=[]
	
	pageLinksList=getAllPageLinks(searchLink)
	
	targPattern=re.compile(pattern)
	
	for i in range(0,len(pageLinksList)):
		if( targPattern.match(pageLinksList[i].text)!=None and "Volume" not in pageLinksList[i].text):#explicitly not downloading BD
			
			if(torrentDownloadObject.getOptions()!=None and torrentDownloadObject.getOptions()=="LatestOnly"):
			
				torrentDownloadObject.pageLinkList.append( pageLinksList[i])
				
				break#first link is the latest

			else:
				torrentDownloadObject.pageLinkList.append(pageLinksList[i])
				
				
			
	
	return torrentDownloadObject


def generateTorLogList():
	torLog=[]
	logList=open(downloadedTorFiles).read().split("\n")
	for i in range(len(logList)-1,-1,-1):
		if(len(logList[i]) >0):
			
			try:
				newDate=logList[i].split(',')[0]
				newFilename=logList[i].split(',')[1]
				newFilename=newFilename[newFilename.rindex("\\")+1:]
				torLog.append(TorLog(newDate , newFilename  ) )
				
			except:
				torLog.append(TorLog( logList[i].split(',')[0], logList[i].split(',')[1]) )
		else:
			logList.remove(logList[i])	
	
	torLog.reverse()
	return torLog


	
def downloadedToday(fileName, torLogList):
	for i in range(0,len(torLogList)):
		if fileName==torLogList[i].filename:
			position=i
			break
	
	logDate=torLogList[position].date
	todaysDate= datetime.datetime.today().strftime(TIME_FORMAT)
	
	
	if (logDate==todaysDate):
		return True
		
	else:
		return False


		
def addToBacklog(torDownloadObj):
	writer=open(downloadTorBackLog,'a')
	
	torDownloadObj.option="Backlog"
	
	writer.write( torDownloadObj.__str__() ) 
	writer.write('\n')
	writer.close()

def getLogFileNames(torLogList):
	return map(operator.attrgetter('filename'), torLogList)
	
		
	
	

def pruneDownloadLinkList(torList):
	#check if file is already downloaded
		
	torLogList=generateTorLogList()
	
	for j in range(len(torList)):
		torList[j].pageLinkList.reverse()
		firstEpisode=True
		for i in range(len(torList[j].pageLinkList)-1,-1,-1):
			
			
			if (torList[j].pageLinkList[i].text in getLogFileNames(torLogList) ):
				
				if (downloadedToday(torList[j].pageLinkList[i].text, torLogList ) == False) and (firstEpisode==True):
					
					print "Adding ", torList[j].pageLinkList[i].text , " to backlog"
					addToBacklog(torList[j])
					torList[j].pageLinkList=[]
					break
				
				
				torList[j].pageLinkList.remove(torList[j].pageLinkList[i])
	
			firstEpisode=False
			
def updateLogFile(downloadedFileName):
	print "Updating download log"
	writer=open(downloadedTorFiles,'a')
	
	today= datetime.date.today()
	dateStr=today.strftime(TIME_FORMAT)
	
	writer.write(dateStr+","+downloadedFileName)
	writer.write('\n')
	
	writer.close()

def removeFromBacklog(torObj):
	rewrite=[]
	for line in open(downloadTorBackLog,'r').readlines():
		if line!=torObj.__str__():
			rewrite.append(line)
	
	for s in rewrite:
		addToBackLog(castBackLogToTorObj(s.split(',')))

def exeDownload(torList):
	for i in range(0,len(torList)):
		for j in range(0,len(torList[i].pageLinkList)):
			
			command="firefox -new-tab " + "\"" + torList[i].pageLinkList[j].get("href").replace("view","download") + "\""
			
			print "Downloading: ", torList[i].pageLinkList[j].text.encode('unicode-escape')
			
			print command
			os.system(command)
			updateLogFile(torList[i].pageLinkList[j].text)
			
			
			
			time.sleep(2)
		
	
if __name__=="__main__":
	TIME_FORMAT="%b/%d/%Y"
	
	prepareForDownload()
	
	downloadObjectList=[]
	day=datetime.date.today().strftime("%A")
	torList=getTorListFromDay(day)	
	for i in xrange(0,len(torList)):
		torList[i]=addLinksAndText(torList[i])
	
	torLog=generateTorLogList()
	
	for tor in torList:
		downloadedThisWeek(tor,torLog)
	
	#pruneDownloadLinkList(torList)
	
	#exeDownload(torList)
	
	print "Finished"
	
	