from sys import stdout, argv
from time import sleep, time, strftime, localtime
from root import hib_log, error_alert
from to_do_list import view_to_do_list
from os import system


def loading_splash(time_limit, output="", splash=None):
    """
    :param time_limit: number of minutes that the splash will run for
    :param output: static text for splash
    :param splash: list of string that will be used as splash

    How writing to stdout works:
    output -> this is output + the first splash string which is empty
    output. -> output + '.' (i.e second splash string)
    output. -> output + \b  (move cursor to previous char)
    output.. -> output. + ".." ('.' from second splash string is overwritten)

    at the end clear the entire splash strings by overwriting with " " char
    then set cursor back to the end of output + 1
    """

    if splash is None:
        splash = ['', '.', "..", "..."]

    i = 0
    start_time = time()

    while (time() - start_time) < time_limit:

        splash_txt = splash[i]
        stdout.write(output + splash_txt)
        sleep(1)
        stdout.write("\r" + len(output + splash_txt) * " " + "\r")

        i += 1
        if i == len(splash):
            i = 0

    print ""


def create_log():
    """Opens hibLog and appends date and time to the file"""

    f = open(hib_log, 'a')
    t = localtime()
    s = " ".join([str(strftime("%B/%d/%Y, %H:%M", t)), '\n'])
    f.write(s)
    f.close()


def hibernate():
    """
    hib_cmd = r"C:\Windows\System32\rundll32.exe " +
    "PowrProf.dll,SetSuspendState"
    """

    hib_cmd = "shutdown /h"
    system(hib_cmd)


def main(time_limit):
    """
    Sets program to sleep for time_limit minutes
    Hibernate log is created after sleep with time stamp
    Calls view_to_do_list to be viewable when resuming from hibernation
    Sets the computer to hibernate

    :param time_limit: time limit in minutes
    """

    for i in range(int(time_limit), 0, -1):
        output = "Time remaining until hibernation: {}".format(str(i))
        loading_splash(60, output)

    create_log()
    hibernate()
    view_to_do_list()


if __name__ == "__main__":

    # windll.kernel32.SetConsoleCtrlHandler(0, 1)  # disables sigint / ctrl + c

    if len(argv) < 2:
        error_alert("Missing time parameter")

    else:
        try:
            main(int(argv[1]))

        except ValueError:
            error_alert("Argument must be an integer")
