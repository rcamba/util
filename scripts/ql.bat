@ECHO OFF

%UtilResources%/jump_dir.py %1 %2 %3
set /p var= <%UtilResources%/logs/directoryQ.log

CD /D %var%
