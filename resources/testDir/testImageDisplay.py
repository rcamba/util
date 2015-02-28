from Tkinter import *
import Image
import ImageTk
import tkMessageBox
from os import listdir, chdir
from random import randint
from time import sleep

def get(event):
	
	if ( entryWidget.get()=="quit"):
		exit()
	#elif (entryWidget.get()=="del"):
	#	entryWidget.delete(0, END)
	
	else:
		print entryWidget.get()
	entryWidget.delete(0, END)#Tkinter.END
	

def displayText():
	

	global entryWidget
	
	if entryWidget.get().strip() == "":
		tkMessageBox.showerror("Tkinter Entry Widget", "Enter a text value")
	else:
		tkMessageBox.showinfo("Tkinter Entry Widget", "Text value =" + entryWidget.get())
	

def runQuiz(master):

	master.title("Hiragana")
	master["padx"] = 40
	master["pady"] = 20   

	# Create a text frame to hold the text Label and the Entry widget
	textFrame = Frame(master)

	#Create a Label in textFrame
	entryLabel = Label(textFrame)
	entryLabel["text"] = "Enter the characters:"
	entryLabel.pack(side=LEFT)

	# Create an Entry Widget in textFrame
	entryWidget = Entry(textFrame)
	entryWidget["width"] = 50
	entryWidget.pack(side=LEFT)
	entryWidget.focus_set()

	entryWidget.bind("<Return>",get)
	entryWidget.pack()
	textFrame.pack()

			
	imageFile = Image.open("FDA6E.jpg")#black
	img = ImageTk.PhotoImage(imageFile)

	imageFile2 = Image.open("fDcXU.jpg")#black
	img2 = ImageTk.PhotoImage(imageFile2)

	
	
	

	canvas.create_image(0,0, anchor=NW, image=img)

	canvas.create_image(img.width()+10,0, anchor=NW, image=img2)

	



	mainloop()

def getImageFileList():
	CHAR_LIST_DIR="C:\\Users\\Kevin\\Pictures\\ScreenShots\\Hiragana\\characters"
	chdir(CHAR_LIST_DIR)
	return listdir(CHAR_LIST_DIR)
	
def createImage(master, imgFileList):
	
	canvas_width=0
	canvas_height=0
	
	master.title("Hiragana")
	master["padx"] = 50
	master["pady"] = 50   
	
	print "Creating images"
	i=0
	randNum=randint(1,4)
	chosenImgs=[]
	while(i<randNum):
		print imgFileList[ randint(0,len(imgFileList)-1) ]
		imageFile=Image.open( imgFileList[ randint(0,len(imgFileList)-1) ] ) 
		img=ImageTk.PhotoImage(imageFile)
		chosenImgs.append(img)
		
		canvas_width+=img.width()
		#canvas_height+=img.height()+5
		
		i=i+1
	
	canvas = Canvas(master, width=canvas_width, height=canvas_height)
	canvas.pack()
	
	startWidth=0
	#chosenImg=chosenImgs[0]
	#canvas.create_image(startWidth, 0, anchor=NW, image=chosenImg)
	
	chosenImg=chosenImgs[0]
	canvas.create_image(0, 0,  image=chosenImg)
	
	startWidth+=img.width()
	"""
	for i in range(0,len(chosenImgs)):
		chosenImg=chosenImgs[i]
		canvas.create_image(startWidth, 0,  image=chosenImg)
		sleep(1)
		startWidth+=img.width()
		print startWidth
	"""
	mainloop()
		
	
master = Tk()

imgFileList=getImageFileList()
createImage(master, imgFileList)

#tMain(master)	


