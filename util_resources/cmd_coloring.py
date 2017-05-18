"""
Recipe by Andre Burgaud
https://www.burgaud.com/bring-colors-to-the-windows-console-with-python/
"""
from ctypes import windll, Structure, c_short, c_ushort, byref
from win32console import STD_OUTPUT_HANDLE, STD_INPUT_HANDLE, STD_ERROR_HANDLE


SHORT = c_short
WORD = c_ushort


class COORD(Structure):
    """struct in wincon.h."""
    _fields_ = [
        ("X", SHORT),
        ("Y", SHORT)]


class SMALL_RECT(Structure):
    """struct in wincon.h."""
    _fields_ = [
        ("Left", SHORT),
        ("Top", SHORT),
        ("Right", SHORT),
        ("Bottom", SHORT)]


class CONSOLE_SCREEN_BUFFER_INFO(Structure):
    """struct in wincon.h."""
    _fields_ = [
        ("dwSize", COORD),
        ("dwCursorPosition", COORD),
        ("wAttributes", WORD),
        ("srWindow", SMALL_RECT),
        ("dwMaximumWindowSize", COORD)]


# wincon.h
COLOR_CHOICES = dict(
    FOREGROUND_BLACK=0x0000,
    FOREGROUND_BLUE=0x0001,
    FOREGROUND_GREEN=0x0002,
    FOREGROUND_CYAN=0x0003,
    FOREGROUND_RED=0x0004,
    FOREGROUND_MAGENTA=0x0005,
    FOREGROUND_YELLOW=0x0006,
    FOREGROUND_GREY=0x0007,
    FOREGROUND_INTENSITY=0x0008,

    BACKGROUND_BLACK=0x0000,
    BACKGROUND_BLUE=0x0010,
    BACKGROUND_GREEN=0x0020,
    BACKGROUND_CYAN=0x0030,
    BACKGROUND_RED=0x0040,
    BACKGROUND_MAGENTA=0x0050,
    BACKGROUND_YELLOW=0x0060,
    BACKGROUND_GREY=0x0070,
    BACKGROUND_INTENSITY=0x0080)

stdout_handle = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
SetConsoleTextAttribute = windll.kernel32.SetConsoleTextAttribute
GetConsoleScreenBufferInfo = windll.kernel32.GetConsoleScreenBufferInfo


def get_console_color():
    """
    Returns the character attributes (colors) of the console screen
    buffer.
    """

    csbi = CONSOLE_SCREEN_BUFFER_INFO()
    GetConsoleScreenBufferInfo(stdout_handle, byref(csbi))
    return csbi.wAttributes


def set_console_color(color):
    """
    Sets the character attributes (colors) of the console screen
    buffer. Color is a combination of foreground and background color,
    foreground and background intensity.
    """

    SetConsoleTextAttribute(stdout_handle, color)
