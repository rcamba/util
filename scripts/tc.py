from root import keyboard_type, get_clipboard_data
from sys import argv


if __name__ == "__main__":

    cData = get_clipboard_data()

    if len(argv) > 1 and "-q" == argv[1]:
        keyboard_type("remote_client.py -rc gat \"")
        keyboard_type(cData)
        keyboard_type("\"")

    else:
        for arg in argv[1:]:
            keyboard_type(arg)
            keyboard_type(" ")
        keyboard_type(cData)
