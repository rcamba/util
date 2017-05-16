@ECHO OFF
start /B /MIN C:\"Program Files (x86)"\VideoLAN\VLC\vlc.exe --qt-start-minimized --one-instance --playlist-enqueue --playlist-autostart --no-crashdump %1 -L
"C:\Program Files\Rainmeter\Rainmeter.exe" !Refresh  Enigma\Sidebar\Music