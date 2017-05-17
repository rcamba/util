from win32com import client
from mouse_macro import rightclick
from subprocess import Popen
from os import path, getenv

if __name__ == "__main__":

    command = path.join(getenv("userprofile"), "Application Data", "Microsoft",
                        "Internet Explorer", "Quick Launch",
                        "Shows Desktop.lnk")
    Popen(command)

    rightclick()
    shell = client.Dispatch("WScript.Shell")
    shell.SendKeys("vd")
