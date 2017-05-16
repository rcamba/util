from copy import copy
from root import reverse_slash, standardize_file
class Tag:

	def __init__(self, newTag):
		self.__tag=newTag
		self.__fileList=[]

	def addToFileList(self, file):
		file=standardize_file(file)
		if file not in self.__fileList:
			self.__fileList.append(str(file))
			self.__fileList=sorted(self.__fileList, key=str.lower)

	def setFileList(self, newFileList):
		self.__fileList=newFileList
		self.__fileList=sorted(self.__fileList, key=str.lower)


		for i in range(len(self.__fileList)-2,-1,-1):
			previous=self.__fileList[i+1]
			curr=self.__fileList[i]

			if curr==previous:
				print "ALERT! Duplicate found. Removing", previous, "from", self.__tag, "tagList"
				self.__fileList.remove(previous)




	def removeFromFileList(self, targetFile):

		targetFound=False

		for file in self.__fileList:
			if standardize_file(file)==standardize_file(targetFile):
				self.__fileList.remove(file)
				targetFound=True
				break


		if targetFound==False:
			print targetFile, " is not in fileList of ", self.__tag, " tag."


		self.__fileList=sorted(self.__fileList, key=str.lower)

	def printFileList(self):
		self.__fileList=sorted(self.__fileList)
		if(len(self.__fileList)>0):
			for i in range(0,len(self.__fileList)):
				print self.__fileList[i]

		else:
			print "Cannot print: fileList is empty"


	def getStringList(self):

		string=""
		self.__fileList=sorted(self.__fileList, key=str.lower)

		if(len(self.__fileList)>0):
			for i in range(0,len(self.__fileList)):
				if(len(self.__fileList[i])>0):
					if i==0:
						string="".join([string,"", reverse_slash(self.__fileList[i], "\\")])
					else:
						string="".join([string,",", reverse_slash(self.__fileList[i], "\\")])
		#else:
		#	print "fileList is empty"

		string=string.strip().lower()
		return string

	def getFileList(self):
		return copy(self.__fileList)

	def getTag(self):
		return self.__tag


