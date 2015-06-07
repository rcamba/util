from win32gui import SendMessage
from win32con import HWND_BROADCAST, WM_SYSCOMMAND


def turnOffMonitor(SC_MONITORPOWER):
	SendMessage(HWND_BROADCAST, WM_SYSCOMMAND, SC_MONITORPOWER, 2)

def turnOnMonitor(SC_MONITORPOWER):
	SendMessage(HWND_BROADCAST, WM_SYSCOMMAND, SC_MONITORPOWER, -1)

if __name__ == "__main__":

	SC_MONITORPOWER = 0xF170
	turnOffMonitor(SC_MONITORPOWER)




