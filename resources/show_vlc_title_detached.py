from os import getpid
from time import sleep
from root import resizeWindow, moveWindow
from mouseMacro import getpos
from get_vlc_title import main as show_vlc_title


if __name__ == "__main__":

	DETACHED_WINDOW_WIDTH = 950
	DETACHED_WINDOW_HEIGHT = 150

	MONITOR_WIDTH_RESOLUTION = 1920
	WIDTH_PCT = 0.75

	HEIGHT_OFFSET_FROM_CURSOR = -200

	CURR_PID = getpid()

	resizeWindow(DETACHED_WINDOW_WIDTH, DETACHED_WINDOW_HEIGHT,
		pid=CURR_PID)

	# if cursor is in the 2nd monitor, place window in center of that monitor
	if getpos()[0] > MONITOR_WIDTH_RESOLUTION:
		#calculate x,y coord to position detached window in middle of  monitor
		x_coord = (int((MONITOR_WIDTH_RESOLUTION * 2) * WIDTH_PCT) -
			(DETACHED_WINDOW_WIDTH / 2))
		y_coord = getpos()[1] + HEIGHT_OFFSET_FROM_CURSOR

		moveWindow(x_coord, y_coord, pid=CURR_PID)

	else:
		x_coord = ((MONITOR_WIDTH_RESOLUTION / 2) -
			(DETACHED_WINDOW_WIDTH / 2))
		y_coord = getpos()[1] + HEIGHT_OFFSET_FROM_CURSOR

		moveWindow(x_coord, y_coord, pid=CURR_PID)

	show_vlc_title()

	#wait two seconds to allow viewing of input since can't toggle - yet
	sleep(2)
