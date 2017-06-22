from time import sleep
from sys import stdout
from ctypes import windll, Structure, c_short, c_ushort, byref
from win32console import STD_OUTPUT_HANDLE

SHORT = c_short
WORD = c_ushort
stdout_handle = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)


class COORD(Structure):
    """struct in wincon.h."""
    _fields_ = [
        ("X", SHORT),
        ("Y", SHORT)]


# noinspection PyPep8Naming
class SMALL_RECT(Structure):
    """struct in wincon.h."""
    _fields_ = [
        ("Left", SHORT),
        ("Top", SHORT),
        ("Right", SHORT),
        ("Bottom", SHORT)]


# noinspection PyPep8Naming
class CONSOLE_SCREEN_BUFFER_INFO(Structure):
    """struct in wincon.h."""
    _fields_ = [
        ("dwSize", COORD),
        ("dwCursorPosition", COORD),
        ("wAttributes", WORD),
        ("srWindow", SMALL_RECT),
        ("dwMaximumWindowSize", COORD)]


GetConsoleScreenBufferInfo = windll.kernel32.GetConsoleScreenBufferInfo
SetConsoleCursorPosition = windll.kernel32.SetConsoleCursorPosition
csbi = CONSOLE_SCREEN_BUFFER_INFO()


def pct_update():
    for i in range(0, 101):
        stdout.write("{}%".format(str(i)))
        stdout.write(len("{}%".format(str(i))) * " " + "\r")
        sleep(0.01)
    print ""


if __name__ == "__main__":
    print 'Start'
    print '\nStop'
    GetConsoleScreenBufferInfo(stdout_handle, byref(csbi))
    csbi.dwCursorPosition.Y -= 2
    csbi.dwCursorPosition.X += 0
    SetConsoleCursorPosition(stdout_handle, csbi.dwCursorPosition)
    pct_update()
