#custrename

from sys import argv
from untag import listAssociatedTags
from os import rename, path, getcwd
from tag import addTag

origName=argv[1]
newName=argv[2]

if( path.isfile(origName)):
	if( path.isabs(origName)==False):
		origName=getcwd() + "\\" +origName
		
	tagList=listAssociatedTags(origName)
	
	if( len(tagList)==0):
		print "No tags found for ", origName
		print "Use normal \"rename\"  command "
		exit()
	
	
	
	
	if path.isabs(newName)==False:
		print path.split(origName)[0] 
		newName= path.split(origName)[0] + "\\" +newName
		
		
	
	rename(origName, newName)
	print "Changed ", origName, " to ", newName

	
	tagInput= ",".join( map(str,tagList))	
	print "Tagged ", newName, " with " , tagInput

	newName="\"" + newName +"\""
	addTag(newName,  tagInput)



else:
	print "Error: Invalid file for first argument"