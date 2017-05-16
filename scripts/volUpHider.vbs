Set oShell = CreateObject ("Wscript.Shell")
Dim strArgs
strArgs= "volUp"
oShell.Run strArgs, 0, false
WScript.Quit