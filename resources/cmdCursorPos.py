from win32api import SetCursorPos
from win32gui import GetWindowRect
from psutil import process_iter
from pywintypes import error as win_type_error
from root import get_hwnds_for_pid
from sys import argv


def get_cmd_hwnd():

    cmd_pid = -1
    cmd_hwnd = -1

    for proc in process_iter():
        if proc.name() == "cmd.exe":
            cmd_pid = proc.pid
            break

    if cmd_pid != -1:
        hwnd_list = get_hwnds_for_pid(cmd_pid)

        cmd_hwnd = hwnd_list[0]

        if len(hwnd_list) > 1:
            print "WARNING: More than one instance of cmd.exe found. " + \
                  "Centered only first cmd.exe"

    else:
        print "cmd.exe not found"

    return cmd_hwnd


def center_cmd():
    """Sets cursor to center of CMD"""
    cmd_hwnd = get_cmd_hwnd()

    try:
        rect = GetWindowRect(cmd_hwnd)
        x_start = rect[0]
        y_start = rect[1]
        width = rect[2] - x_start
        height = rect[3] - y_start

        x = (width / 2) + x_start
        y = (height / 2) + y_start

        SetCursorPos([x, y])

    except win_type_error, e:
        print "cmd_hwnd not found"
        print e.message
        print str(e)


if __name__ == '__main__':

    if len(argv) == 1:
        center_cmd()

    else:
        if len(argv) == 2:
            x = int(argv[1].split(',')[0])
            y = int(argv[1].split(',')[1])
        elif len(argv) == 3:
            x = int(argv[1])
            y = int(argv[2])

        SetCursorPos([x, y])
