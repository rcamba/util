@ECHO OFF

%UtilResources%/dirJump.pyc %1 %2 %3
set /p var= <%UtilResources%/logs/directoryQ.log

CD /D %var%
