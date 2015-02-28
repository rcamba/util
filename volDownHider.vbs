Set oShell = CreateObject ("Wscript.Shell")
Dim strArgs
strArgs= "volDown"
oShell.Run strArgs, 0, false
WScript.Quit