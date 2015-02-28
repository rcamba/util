@ECHO OFF

set /p var= <%UtilResources%/prevDir.txt


REM this will delete the top in the queue
REM java popDir d

CD /D %var%
