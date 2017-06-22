from subprocess import Popen
from sys import argv
from hib import loading_splash
from pipes import quote

if __name__ == "__main__":

    time_left = int(argv[1])

    argv = argv[2:]
    command = quote(" ".join(map(str, argv)))

    for i in range(int(time_left), 0, -1):
        output = "Executing {c} in {tl} minute(s)".format(
            c=command, tl=time_left)
        loading_splash(60, output)

    Popen(command, shell=True)
