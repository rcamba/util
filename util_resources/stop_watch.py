from msvcrt import kbhit, getch
from sys import stdout
from datetime import datetime
from root import print_colored


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
    start_prompt = "Press any key to START the timer"
    stdout.write(start_prompt)

    wait_for_keypress()

    init_time = datetime.now()

    stdout.write("\r" + len(start_prompt) * " " + "\r")
    stdout.write("Press any key to ")
    print_colored("STOP", "red")
    stdout.write(" the timer\n")

    print_time(init_time)


if __name__ == "__main__":
    main()
