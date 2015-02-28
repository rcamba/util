import win32gui
currFocusHwnd = win32gui.GetForegroundWindow()

win32gui.SetForegroundWindow(currFocusHwnd)