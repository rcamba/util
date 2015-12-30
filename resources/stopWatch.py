#stopWatch
from msvcrt import kbhit, getch
from time import time
from sys import stdout
from collections import OrderedDict

def wait_for_keypress():
	if (kbhit() == False):
		getch()

	return True

def create_time_diff_str(init_time):
	DECIMAL_ROUNDING = 3
	time_diff = time()-init_time
	rounded_time_diff = round(time_diff, DECIMAL_ROUNDING)

	time_dict = OrderedDict({
		" seconds" : 0.1,
		" minute(s)" : 60.0,
		" hour(s)"  : 60.0
	})

	time_diff_str = ""
	counter = 0
	divisor = time_dict.values()[counter]
	while ((rounded_time_diff/divisor) >= 1.0):
		rounded_time_diff = round((rounded_time_diff/divisor), DECIMAL_ROUNDING)

		counter += 1
		divisor = time_dict.values()[counter]

	time_diff_str = str(rounded_time_diff) + time_dict.keys()[counter-1]

	return time_diff_str

def print_time(init_time):

	while kbhit() == False:

		time_diff_str = create_time_diff_str(init_time)

		stdout.write(time_diff_str)
		stdout.write(len(time_diff_str)*"\b")


def main():

	print "Press any key to START the timer"
	wait_for_keypress()

	init_time = time()

	print "Press any key to STOP the timer"
	print_time(init_time)


if __name__ == "__main__":
	main()