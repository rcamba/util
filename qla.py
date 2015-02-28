from root import quickLaunchFile
from os import getcwd
f=open(quickLaunchFile,"a")

f.write(str( getcwd() ) )
f.close()