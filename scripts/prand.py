"""
Using .py because .bat reads commas as a separator/delimiter
"""

from sys import argv
from os import system

if __name__ == "__main__":
    stringArgs = " ".join(map(str, argv[1:]))
    system("".join(["%Util%/util_resources/prandom.py ", stringArgs]))
