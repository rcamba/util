#toDoList
#CatFoodForPrawnGuns

from sys import argv, exit as sys_exit
from datetime import date
from root import toDoListTextFile, switchBoard, printNumberedList, createBackUp, setClipboardData, chooseFromNumberedList

AVAILABLE_SWITCHES=['a','v','d','s']

class ToDoTask:
	
	def __init__(self, task, date=date.today().strftime("%b %d, %Y")):
		self.__date=date
		self.__task=task
		
	def getDate(self):
		return self.__date
	
	def getTask(self):
		return self.__task
	
	def __str__(self):
		return "".join([ self.getDate(), '\t', self.getTask() ])
		#return "".join([ self.getDate(), '    ', self.getTask() ])


def addItem(newTask):
	
	newTask=ToDoTask(newTask)
	writer=open(toDoListTextFile,'a')
	writer.write('\n')
	writer.write( str("".join([newTask.getDate(),"\t",newTask.getTask()])) )
	writer.close()

def deleteItem(taskList,numberOfItem):
	
	print "Removing:\n\t", str(numberOfItem)+")", taskList[numberOfItem-1].getDate(), "\t", taskList[numberOfItem-1].getTask()
	taskList.remove(taskList[numberOfItem-1])
	
	
	writer=open(toDoListTextFile,'w')
	for task in taskList:
		if isinstance(task, ToDoTask)==True:
			writer.write( str("".join([task.getDate(),"\t",task.getTask()])) )
			if taskList.index(task)!=len(taskList)-1:
				writer.write('\n')
	writer.close()
	
	
def viewToDoList(taskList):
	for i in range(0,len(taskList)):
		taskList[i]=taskList[i].__str__()
	printNumberedList(taskList)	
	
if __name__=="__main__":
	
	switches=switchBoard(argv)
	createBackUp(toDoListTextFile)
	
	
	taskList=open(toDoListTextFile).read().split('\n')
	for i in range(0,len(taskList)):
		if len(taskList[i])>0:
			taskList[i]=ToDoTask(taskList[i].split('\t')[1], taskList[i].split('\t')[0])
		
	
	if 'a' in switches:
		if len(argv)>1:
			addItem(" ".join(map(str,argv[1:])))
		else:
			task=raw_input("\nEnter task argument: ")
			if len(task)>1:
				addItem(task)
			
	
	elif 'd' in switches:
		deleteItem(taskList, int(argv[1]))
	
	elif 'v' in switches:
		viewToDoList(taskList)
		
		if 's' in switches:
		
			try:
				chosenNum=chooseFromNumberedList(taskList)
				result=taskList[chosenNum].getTask()
				#print result
				setClipboardData(result)
			except IndexError:
				raise
				print "Number ", argv[1], "  is out of bounds."
		