from os import getpid
from time import sleep
from root import resize_window, move_window
from mouse_macro import getpos
from get_vlc_title import get_vlc_title
from ctypes import windll

if __name__ == "__main__":

    windll.kernel32.SetConsoleTitleA("vlc title detached")
    DETACHED_WINDOW_WIDTH = 950
    DETACHED_WINDOW_HEIGHT = 150

    MONITOR_WIDTH_RESOLUTION = windll.user32.GetSystemMetrics(0)
    WIDTH_PCT = 0.75

    HEIGHT_OFFSET_FROM_CURSOR = -200

    CURR_PID = getpid()

    resize_window(CURR_PID, DETACHED_WINDOW_WIDTH, DETACHED_WINDOW_HEIGHT)

    # if cursor is in the 2nd monitor, place window in center of that monitor
    if getpos()[0] > MONITOR_WIDTH_RESOLUTION:
        # calculate x,y coord to position detached window in middle of  monitor
        # assumes that the monitors have the same resolution...
        x_coord = (int((MONITOR_WIDTH_RESOLUTION * 2) * WIDTH_PCT) -
                   (DETACHED_WINDOW_WIDTH / 2))
        y_coord = getpos()[1] + HEIGHT_OFFSET_FROM_CURSOR

        move_window(CURR_PID, x_coord, y_coord)

    else:
        x_coord = ((MONITOR_WIDTH_RESOLUTION / 2) -
                   (DETACHED_WINDOW_WIDTH / 2))
        y_coord = getpos()[1] + HEIGHT_OFFSET_FROM_CURSOR

        move_window(CURR_PID, x_coord, y_coord)

    fp = get_vlc_title()
    if fp == ".":
        pass

    # wait two seconds to allow viewing of input since can't toggle - yet
    sleep(2)
