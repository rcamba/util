from msvcrt import kbhit, getch
from sys import stdout
from datetime import datetime


def wait_for_keypress():

    if kbhit() == 0:
        getch()

    return True


def create_time_diff_str(init_time):

    time_diff = datetime.now() - init_time
    time_diff_str = str(time_diff)[:-3]

    return time_diff_str


def print_time(init_time):

    prev_time_diff_str = ""

    while kbhit() == 0:
        time_diff_str = create_time_diff_str(init_time)
        if time_diff_str != prev_time_diff_str:
            stdout.write(time_diff_str + len(time_diff_str) * " " + "\r")
            stdout.write(len(time_diff_str) * "\b")
            stdout.flush()
            prev_time_diff_str = time_diff_str
    getch()


def main():

    print "Press any key to START the timer"
    wait_for_keypress()

    init_time = datetime.now()

    print "Press any key to STOP the timer"
    print_time(init_time)


if __name__ == "__main__":
    main()
