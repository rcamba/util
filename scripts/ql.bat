@ECHO OFF

%Util%/resources/jump_dir.py %1 %2 %3
set /p var= <%Util%/logs/directoryQ.log

CD /D %var%
