
from root import get_console_color, set_console_color
from msvcrt import kbhit, getch
res=""
occ=get_console_color()
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
            set_console_color("red")
        else:
            set_console_color(occ)
        print res

set_console_color(occ)
