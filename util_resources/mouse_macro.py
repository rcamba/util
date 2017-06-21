"""
Author: jtokarchuk
https://github.com/jtokarchuk/MouseTab/blob/master/mousemacro.py

click() -- calls left mouse click
hold() -- presses and holds left mouse button
release() -- releases left mouse button

rightclick() -- calls right mouse click
righthold() -- calls right mouse hold
rightrelease() -- calls right mouse release

middleclick() -- calls middle mouse click
middlehold() -- calls middle mouse hold
middlerelease() -- calls middle mouse release

move(x,y) -- moves mouse to x/y coordinates (in pixels)
getpos() -- returns mouse x/y coordinates (in pixels)
slide(x,y) -- slides mouse to x/y coodinates (in pixels)
              also supports optional speed='slow', speed='fast'
"""
from _ctypes import Structure, POINTER, Union, byref, sizeof, pointer
from ctypes import c_ulong, c_ushort, c_short, c_long, windll
from time import sleep
from argparse import ArgumentParser


__all__ = ['click', 'hold', 'release',
           'rightclick', 'righthold', 'rightrelease',
           'middleclick', 'middlehold', 'middlerelease',
           'move', 'slide', 'getpos']

# START SENDINPUT TYPE DECLARATIONS
PUL = POINTER(c_ulong)


class KeyBdInput(Structure):
    _fields_ = [("wVk", c_ushort),
                ("wScan", c_ushort),
                ("dwFlags", c_ulong),
                ("time", c_ulong),
                ("dwExtraInfo", PUL)]


class HardwareInput(Structure):
    _fields_ = [("uMsg", c_ulong),
                ("wParamL", c_short),
                ("wParamH", c_ushort)]


class MouseInput(Structure):
    _fields_ = [("dx", c_long),
                ("dy", c_long),
                ("mouseData", c_ulong),
                ("dwFlags", c_ulong),
                ("time", c_ulong),
                ("dwExtraInfo", PUL)]


class InputI(Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]


class Input(Structure):
    _fields_ = [("type", c_ulong),
                ("ii", InputI)]


class POINT(Structure):
    _fields_ = [("x", c_ulong),
                ("y", c_ulong)]
# END SENDINPUT TYPE DECLARATIONS

#  LEFTDOWN   = 0x00000002,
#  LEFTUP     = 0x00000004,
#  MIDDLEDOWN = 0x00000020,
#  MIDDLEUP   = 0x00000040,
#  MOVE       = 0x00000001,
#  ABSOLUTE   = 0x00008000,
#  RIGHTDOWN  = 0x00000008,
#  RIGHTUP    = 0x00000010

MIDDLEDOWN = 0x00000020
MIDDLEUP = 0x00000040
MOVE = 0x00000001
ABSOLUTE = 0x00008000
RIGHTDOWN = 0x00000008
RIGHTUP = 0x00000010


FInputs = Input * 2
extra = c_ulong(0)

click = InputI()
click.mi = MouseInput(0, 0, 0, 2, 0, pointer(extra))
release = InputI()
release.mi = MouseInput(0, 0, 0, 4, 0, pointer(extra))

x1 = FInputs((0, click), (0, release))

x2 = FInputs((0, click))

x3 = FInputs((0, release))


def move(x, y):
    windll.user32.SetCursorPos(x, y)


def getpos():
    global pt
    pt = POINT()
    windll.user32.GetCursorPos(byref(pt))
    return pt.x, pt.y


def slide(a, b, speed=0):
    while True:
        if speed == 'slow':
            sleep(0.005)
            t_speed = 2
        if speed == 'fast':
            sleep(0.001)
            t_speed = 5
        if speed == 0:
            sleep(0.001)
            t_speed = 3

        x = getpos()[0]
        y = getpos()[1]
        if abs(x - a) < 5:
            if abs(y - b) < 5:
                break

        if a < x:
            x -= t_speed
        if a > x:
            x += t_speed
        if b < y:
            y -= t_speed
        if b > y:
            y += t_speed
        move(x, y)


def click():
    windll.user32.SendInput(2, pointer(x1), sizeof(x1[0]))


def hold():
    windll.user32.SendInput(2, pointer(x2), sizeof(x2[0]))


def release():
    windll.user32.SendInput(2, pointer(x3), sizeof(x3[0]))


def rightclick():
    windll.user32.mouse_event(RIGHTDOWN, 0, 0, 0, 0)
    windll.user32.mouse_event(RIGHTUP, 0, 0, 0, 0)


def righthold():
    windll.user32.mouse_event(RIGHTDOWN, 0, 0, 0, 0)


def rightrelease():
    windll.user32.mouse_event(RIGHTUP, 0, 0, 0, 0)


def middleclick():
    windll.user32.mouse_event(MIDDLEDOWN, 0, 0, 0, 0)
    windll.user32.mouse_event(MIDDLEUP, 0, 0, 0, 0)


def middlehold():
    windll.user32.mouse_event(MIDDLEDOWN, 0, 0, 0, 0)


def middlerelease():
    windll.user32.mouse_event(MIDDLEUP, 0, 0, 0, 0)


if __name__ == '__main__':
    parser = ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-c", "--click", action="store_true", help="click at current cursor pos")
    group.add_argument("-dc", "--double-click", action="store_true", help="double click at current cursor pos")
    group.add_argument("-g", "--get-pos", action="store_true", help="print current x,y coordinates of cursor")
    group.add_argument("-rc", "--right-click", action="store_true", help="right click at current cursor pos")

    args = parser.parse_args()
    if args.click:
        click()
    elif args.double_click:
        click()
        click()
    elif args.get_pos:
        print getpos()
    elif args.right_click:
        rightclick()
