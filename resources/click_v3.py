#c3


from mouseMacro import *
from root import takeScreenshot

from ImageChops import difference
from PIL import Image # py2.7PIL.exe

from os import system

from time import sleep



def __refreshPage__():
	
	
	move(SEARCH_LOCATION[0], SEARCH_LOCATION[1])
	click()
	
	
def __base_equal_to_SS__():
	
	image1=Image.open(BASE_IMAGE)
	image2=Image.open(ssFileName)
	
	
	return difference(image1, image2).getbbox() is None
	
def bess(im1,im2):
	
	image1=Image.open(im1)
	image2=Image.open(im2)
	
	
	return difference(image1, image2).getbbox() is None
	
	

if __name__ == "__main__":
		
	browser="firefox" # "chrome"

	SEARCH_LOCATION=(1468,46)#(0,0)
	BASE_IMAGE="./basePicture.png"

	while 1:
		

		__refreshPage__()
		sleep(2)
		ssFileName=takeScreenshot(browser)
		if __base_equal_to_SS__()==False:
			print "Deleted similar screenshot to base picture"
			system("del " + ssFileName) #only keep screenshots that are the different
		
		sleep(5)
