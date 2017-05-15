from root import keyboardType, getClipboardData
from sys import argv


if __name__ == "__main__":

    cData = getClipboardData()

    if len(argv) > 1 and "-q" == argv[1]: # add config option for extra string before text or maybe something like regex pattern
        keyboardType("remote_client.py -qbit \"")
        keyboardType(cData)
        keyboardType("\"")

    else:
        for arg in argv[1:]:
            keyboardType(arg)
            keyboardType(" ")
        keyboardType(cData)
