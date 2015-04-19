#GAT:
from root import getAllPageLinks, downloadedTorFiles, printNumberedList, downloadTorBackLog, createBackUp
import re
import datetime
import os
import time
import operator 
class TorrentDownload:
	def __init__(self,newPattern,newFansub_ID,newSearchTerms="",newOption=""):
		self.origPattern=newPattern
		self.fansub_ID=newFansub_ID
		
		if len(newSearchTerms)==0:
			self.searchTerms=newPattern.replace(' ','+')
		else:
			self.searchTerms=newSearchTerms.replace(' ','+')
			
		self.pattern=self.origPattern.replace(' ','.+')
		self.pattern='.+'+self.pattern+'.+'
		
		if(len(newOption)>0):
			self.option=newOption
		else:
			self.option=None
		
		self.pageLinkList=[]

	def getPatternStr(self):
		return self.origPattern
	
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

def downloadedThisWeek(pattern, torLogList):
	retVal=False
	
	targPattern=re.compile(pattern)
	
	today=datetime.date.today()
	lastMon=(today - datetime.timedelta(days=today.weekday()))#last monday
	#thisSun=(today + datetime.timedelta(days=-today.weekday()-1, weeks=1)).strftime(TIME_FORMAT)#coming sunday
	
	startSlice=0;
	
	for log in torLogList:
		logDateObj=datetime.datetime.strptime(log.date, TIME_FORMAT).date()
		if logDateObj>=lastMon and startSlice==0:
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
				print "Downloaded THIS WEEK: ", tor.getPatternStr()
				torList.remove(tor)
		else:
			if( downloadedToday(tor.getPattern(),torLogList) ==True):
				print "Downloaded TODAY: ", tor.getPatternStr()
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
	VIVID_ID=209076
	
	if day=="Monday":
		torList.append( 
			TorrentDownload("Punch Line 720", HORRIBLESUBS_ID,"Punch Line")
		)
		
		torList.append(
			TorrentDownload("Arslan Senki 720", HORRIBLESUBS_ID)
		)
		
		torList.append( 
			TorrentDownload("Ghost Shell 720", HORRIBLESUBS_ID)
		)
		
		torList.append( 
			TorrentDownload("Yamada 720", HORRIBLESUBS_ID, "Yamada")
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
			TorrentDownload("Kekkai Sensen", VIVID_ID, "Kekkai Sensen")
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
			TorrentDownload("Saenai Heroine no Sodatekata", FFF_ID, "Saenai Heroine no Sodatekata")
		)
		
		torList.append( 
			TorrentDownload("Naruto Shippuuden 720", HORRIBLESUBS_ID, "Naruto Shippuuden", "LatestOnly")
		)
	
	elif day=="Friday":
		
		torList.append( 
			TorrentDownload("Yahari Ore no Seishun Love Come wa. Zoku", FFF_ID, "Yahari Ore no Seishun Love Come wa ")
		)
		
		torList.append(
			TorrentDownload("Assassination Classroom 720", HORRIBLESUBS_ID, "Assassination Classroom")
		)
		
		torList.append(
			TorrentDownload("Gunslinger Stratos 720", HORRIBLESUBS_ID, "Gunslinger Stratos")
		)
		
		torList.append(
			TorrentDownload("Ninja Slayer 720", HORRIBLESUBS_ID, "Ninja Slayer")
		)
		
		torList.append(
			TorrentDownload("Triage 720", HORRIBLESUBS_ID, "Triage")
		)
		
		
		torList.append( 
			TorrentDownload("Mikagura School Suite", CAFFEINE_ID, "Mikagura School Suite")
		)
		
			
	elif day=="Saturday":
		torList.append( 
			TorrentDownload("Shokugeki", FFF_ID, "Shokugeki")
		)
		 
		
		torList.append( 
			TorrentDownload("Kuroko 720", HORRIBLESUBS_ID, "Kuroko")
		)
		
		torList.append( 
			TorrentDownload("Fate Unlimited", COMMIE_ID, "Fate Unlimited")
		)

	return torList
			
def addLinksAndText(torrentDownloadObject):
	pattern=torrentDownloadObject.getPattern()
	searchUser=torrentDownloadObject.getFansubID()
	searchTerm=torrentDownloadObject.getSearchTerms()
	searchLink="http://www.nyaa.se/?page=search&cats=0_0&filter=0&term="+searchTerm+"&user="+ searchUser
	#print searchLink
	resultList=[]
	
	pageLinksList=getAllPageLinks(searchLink)
	
	targPattern=re.compile(pattern)
	fll=filenameLogList()
	for i in range(0,len(pageLinksList)):
		if( targPattern.match(pageLinksList[i].text)!=None and "Volume" not in pageLinksList[i].text and pageLinksList[i].text not in fll):#explicitly not downloading BD
			
			if(torrentDownloadObject.getOptions()=="LatestOnly"):
			
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


def getLogFileNames(torLogList):
	return map(operator.attrgetter('filename'), torLogList)

def updateLogFile(updateLogList):
	if len(updateLogList)>0:
		print "Updating download log"
		createBackUp(downloadedTorFiles)
		writer=open(downloadedTorFiles,'a')
		
		today= datetime.date.today()
		dateStr=today.strftime(TIME_FORMAT)
		
		for uLog in updateLogList:
			writer.write(dateStr+","+uLog)
			writer.write('\n')
		
		writer.close()

def exeDownload(finalTorList):
	updateLogList=[]
	for i in range(0,len(finalTorList)):
		for j in range(0,len(finalTorList[i].pageLinkList)):
			
			command="firefox -new-tab " + "\"" + finalTorList[i].pageLinkList[j].get("href").replace("view","download") + "\""
			
			print "Downloading: ", finalTorList[i].pageLinkList[j].text.encode('unicode-escape'), "\n"
	
			os.system(command)
			updateLogList.append(finalTorList[i].pageLinkList[j].text)

			time.sleep(2)
		if len(finalTorList[i].pageLinkList)==0:
			print "No new torrent for", finalTorList[i].getPatternStr()
			
	updateLogFile(updateLogList)

def filenameLogList():
	f=[]
	for log in torLogList:
		f.append(log.filename)
	
	return f
	

	
	return finalTorList
if __name__=="__main__":
	TIME_FORMAT="%b/%d/%Y"
	
	prepareForDownload()
	
	torList=[]
	finalTorList=[]
	
	torLogList=generateTorLogList()
	today=datetime.date.today()
	todayInWeekdayDecimal= int(today.strftime("%w"))
	print "Gathering torrent targets"
	dayArray=["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
	for i in range(1, todayInWeekdayDecimal+1): #0 is sunday
		day=dayArray[i]
		#(today - datetime.timedelta(days=today.weekday()-1+i)).strftime("%A")
		torList= getTorListFromDay(day)
		
		if i==todayInWeekdayDecimal:
			finalTorList.extend( handleBacklogs(torList, torLogList, True))
		
		else:
			finalTorList.extend( handleBacklogs(torList, torLogList, False))
	
	print "Finding links for torrents"
	for i in xrange(0,len(finalTorList)):
		finalTorList[i]=addLinksAndText(finalTorList[i])
	

	
	print "Starting downloads"
	exeDownload(finalTorList)
	
	print "Finished"
