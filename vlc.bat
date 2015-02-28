@ECHO OFF
start /B /MIN C:\"Program Files (x86)"\VideoLAN\VLC\vlc.exe --qt-start-minimized --one-instance --playlist-enqueue --playlist-autostart --no-crashdump %1 -L
REM start /B /MIN C:\"Program Files (x86)"\VideoLAN\VLC\vlc.exe --qt-start-minimized --one-instance --global-key-play-pause=Shift+2 --global-key-prev=Shift+1 --global-key-next=Shift+3 --playlist-enqueue --playlist-autostart %1 -L
REM start /B /MIN C:\"Program Files (x86)"\VideoLAN\VLC\vlc.exe --qt-start-minimized --one-instance --global-key-play-pause=5 --global-key-prev=4 --global-key-next=6 --playlist-enqueue --playlist-autostart %1 -L
REM start /B /MIN C:\"Program Files"\VideoLAN\VLC\vlc.exe --qt-start-minimized --one-instance --global-key-play-pause=5 --global-key-prev=4 --global-key-next=6 --playlist-enqueue --playlist-autostart %1 -L
"C:\Program Files\Rainmeter\Rainmeter.exe" !Refresh  Enigma\Sidebar\Music


