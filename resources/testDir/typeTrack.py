
from root import getConsoleColor, setConsoleColor
from msvcrt import kbhit, getch
res=""
occ=getConsoleColor()
tagList=["red","blue","1red1"]
userIn=-1
while userIn!=13:
    if kbhit():
        charG=getch()
        userIn= ord(charG)

        if userIn==8:
            res=res[:-1]
        else:
            res=res+charG
        if res not in tagList:
            setConsoleColor("red")
        else:
            setConsoleColor(occ)
        print res

setConsoleColor(occ)
