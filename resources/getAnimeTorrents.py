#GAT:

from root import getAllPageLinks, downloadedTorFiles, printNumberedList, downloadTorBackLog
import re
import datetime
import os
import time
import operator 
class TorrentDownload:
	def __init__(self,newPattern,newFansub_ID,newSearchTerms,newOption=""):
		self.origPattern=newPattern
		self.fansub_ID=newFansub_ID
		self.searchTerms=newSearchTerms.replace(' ','+')
		
		self.pattern=self.origPattern.replace(' ','.+')
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
			return ", ".join([str(self.origPattern), str(self.fansub_ID), str(self.searchTerms), str(self.option)])
		else:
			return ", ".join([str(self.origPattern), str(self.fansub_ID), str(self.searchTerms)])

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
	
def downloadedThisWeek(pattern, torLogList):
	retVal=False
	
	targPattern=re.compile(pattern)
	
	today=datetime.date.today()
	lastMon=(today - datetime.timedelta(days=today.weekday())).strftime(TIME_FORMAT)#last monday
	thisSun=(today + datetime.timedelta(days=-today.weekday()-1, weeks=1)).strftime(TIME_FORMAT)#coming sunday
	
	startSlice=0;
	
	for log in torLogList:
		if log.date==lastMon and startSlice==0:
			startSlice=torLogList.index(log)
		
	endSlice=len(torLogList)
	torLogList=torLogList[startSlice:endSlice]
	for log in torLogList:
		if targPattern.match(log.filename):
			retVal=True
			break
	
	return retVal

def downloadedToday(pattern, torLogList):
	retVal=False
	
	todaysDate=datetime.date.today().strftime(TIME_FORMAT)
	position=-1
	targPattern=re.compile(pattern)
	for i in range(0,len(torLogList)):
		if todaysDate==torLogList[i].date:
			position=i
			break
	
	if position>-1:
		for i in range(position, len(torLogList)):
			if targPattern.match(torLogList[i].filename):
				retVal=True
	

	return retVal
	
def handleBacklogs(torList, torLogList, today=False):
	

	for tor in torList[:]:
		
		
		#if already downloaded remove from list, no need to download it
		
		if today==False:
			if( downloadedThisWeek(tor.getPattern(), torLogList) ==True):
				print "Downloaded THIS WEEK: ", tor.getPattern()
				torList.remove(tor)
		else:
			
			if( downloadedToday(tor.getPattern(),torLogList) ==True):
				print "Downloaded TODAY: ", tor.getPattern()
				torList.remove(tor)
			
	return torList
	
def getTorListFromDay(day):
	
	torList=[]
	
	HORRIBLESUBS_ID=64513
	COMMIE_ID=76430
	UNDERWATER_ID=265
	DAMEDESUYO_ID=227008
	FFF_ID=73859
	CAFFEINE_ID=284035
	VIVID_ID=678163
	
	if day=="Monday":
		torList.append( 
			TorrentDownload("Punch Line 720", HORRIBLESUBS_ID, "Punch Line")
		)
		
		torList.append(
			TorrentDownload("Arslan Senki 720", HORRIBLESUBS_ID, "Arslan Senki")
		)
		
		torList.append( 
			TorrentDownload("Ghost Shell 720", HORRIBLESUBS_ID, "Ghost")
		)
		
		torList.append( 
			TorrentDownload("Yamada 720", HORRIBLESUBS_ID, "Yamada")
		)
		
		torList.append( 
			TorrentDownload(" Grisaia no Meikyuu 720", HORRIBLESUBS_ID, " Grisaia no Meikyuu")
		)
		
		torList.append( 
			TorrentDownload("Owari", DAMEDESUYO_ID, "Owari")
		) 
		
	
	if day=="Tuesday": 
		torList.append( 
			TorrentDownload("Nagato", CAFFEINE_ID, "Nagato")
		)
		
		
		
		torList.append( 
			TorrentDownload("Plastic", COMMIE_ID, " ")
		) 
		
		torList.append( 
			TorrentDownload("Hibike Euphonium", FFF_ID, " ")
		)
		
		torList.append( 
			TorrentDownload("Kekkai Sensen ", VIVID_ID, "Kekkai Sensen ")
		)
		
		torList.append( 
			TorrentDownload("Highschool DxD BorN", FFF_ID, "Highschool DxD BorN")
		)
		
	elif day=="Wednesday":
		torList.append( 
			TorrentDownload("Nisekoi", COMMIE_ID, "Nisekoi 2")
		)
		
		
	elif day=="Thursday":
		torList.append( 
			TorrentDownload("Saekano", FFF_ID, "Saekano")
		)
		
		torList.append( 
			TorrentDownload("Naruto Shippuuden 720", HORRIBLESUBS_ID, "Naruto Shippuuden", "LatestOnly")
		)
		
		
		
		
	elif day=="Friday":
		
		torList.append( 
			TorrentDownload("Yahari Ore no Seishun Love Come wa ", FFF_ID, "Yahari Ore no Seishun Love Come wa ")
		)
		
		
		torList.append( 
			TorrentDownload("Assassination Classroom 720", HORRIBLESUBS_ID, "Assassination Classroom")
		)
			
	elif day=="Saturday":
		
		
		torList.append( 
			TorrentDownload("Kuroko 720", HORRIBLESUBS_ID, "Kuroko")
		)
		
		torList.append( 
			TorrentDownload("Fate", COMMIE_ID, "Fate")
		)
		
		
		
		
			
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
	
	
	torList=[]
	finalTorList=[]
	
	torLogList=generateTorLogList()
	today=datetime.date.today()
	todayInWeekdayDecimal= int(today.strftime("%w"))
	
	for i in range(0, todayInWeekdayDecimal): #0 is sunday
		day=(today - datetime.timedelta(days=today.weekday()-1+i)).strftime("%A")
		torList= getTorListFromDay(day)
		
		if i==todayInWeekdayDecimal-1:
			print i
			finalTorList.extend( handleBacklogs(torList, torLogList, False))
		
		else:
			finalTorList.extend( handleBacklogs(torList, torLogList, True))
	
	#for f in finalTorList:
		#print f
	
	for i in xrange(0,len(finalTorList)):
		finalTorList[i]=addLinksAndText(finalTorList[i])
		#print finalTorList[i]
	
	exeDownload(finalTorList)
	
	print "Finished"
	
	