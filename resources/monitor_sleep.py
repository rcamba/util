from win32gui import SendMessage
from win32con import HWND_BROADCAST, WM_SYSCOMMAND


def turn_off_monitor(SC_MONITORPOWER):
    SendMessage(HWND_BROADCAST, WM_SYSCOMMAND, SC_MONITORPOWER, 2)


def turn_on_monitor(SC_MONITORPOWER):
    SendMessage(HWND_BROADCAST, WM_SYSCOMMAND, SC_MONITORPOWER, -1)

if __name__ == "__main__":

    SC_MONITORPOWER = 0xF170
    turn_off_monitor(SC_MONITORPOWER)
