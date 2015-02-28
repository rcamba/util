@ECHO OFF


REM CD C:\Users\Kevin\Util\resources

REM this switches top with the parameter if paramater is available
REM java popDir %1

%UtilResources%/quickLaunch.pyc %1
set /p var= <%UtilResources%/directoryQ.txt


REM this will delete the top in the queue
REM java popDir d

CD /D %var%
