import os
import sys
import json
import time
import subprocess
import win32gui


from root import strack_log, keyboard_type, get_hwnds_for_pid


def load_series_dict():
    with open(strack_log) as reader:
        series_dict = json.load(reader)
    return series_dict


def write_series_dict(series_dict):
    with open(strack_log, "w") as writer:
        json.dump(series_dict, writer, indent=2, separators=(',', ': '))


def add_to_series_dict(series_path):
    if not os.path.isabs(series_path) or not os.path.isdir(series_path):
        raise IOError("{f} is not in absolute path or not a directory".format(f=series_path))
    series_dict = load_series_dict()
    series_path = os.path.realpath(series_path)
    if series_path not in series_dict:
        f_list = os.listdir(series_path)
        series_dict[series_path] = f_list
        write_series_dict(series_dict)
        print "Added:", series_path
    else:
        print "{} has already been added".format(series_path)


def get_media_player_path():
    vlc_exe_path = os.path.join(os.getenv("PROGRAMFILES"), "VideoLAN", "VLC", "vlc.exe")
    if not os.path.isfile(vlc_exe_path):
        vlc_exe_path = os.path.join(os.getenv("PROGRAMFILES(x86)"), "VideoLAN", "VLC", "vlc.exe")
    if not os.path.isfile(vlc_exe_path):
        raise IOError("VLC player not found")

    return vlc_exe_path


def play_series(series_dict, series_path):
    def input_prompt():
        return raw_input("[{next}] to play next file or [{quit}] to quit program\n".format(
            next=next_key_press, quit=quit_key_press)).lower()

    next_key_press = "n"
    quit_key_press = "q"
    user_input = next_key_press
    valid_inputs = [next_key_press, quit_key_press]
    first_run = True
    vlc_opts = "--one-instance"
    while user_input != quit_key_press and series_path in series_dict:
        if user_input == next_key_press:
            play_now = series_dict[series_path].pop(0)
            print play_now
            if first_run:
                proc = subprocess.Popen([get_media_player_path(), vlc_opts,
                                         os.path.join(series_path, play_now)])
                while len(get_hwnds_for_pid(proc.pid)) == 0:
                    time.sleep(1)

                keyboard_type("f", proc.pid)  # fullscreen

            else:
                subprocess.Popen([get_media_player_path(), vlc_opts,
                                  os.path.join(series_path, play_now)])

                # noinspection PyUnboundLocalVariable
                win32gui.SetForegroundWindow(get_hwnds_for_pid(proc.pid)[0])
                keyboard_type("n", proc.pid)  # fullscreen

            if len(series_dict[series_path]) == 0:
                del series_dict[series_path]

            first_run = False
            write_series_dict(series_dict)

        user_input = input_prompt()
        while user_input not in valid_inputs:
            print "Invalid input: {}".format(user_input)
            user_input = input_prompt()

    proc.terminate()
    print "End"


if __name__ == "__main__":
    if len(sys.argv) == 2:
        if str(sys.argv[1]).isdigit():
            s_dict = load_series_dict()
            play_series(s_dict, s_dict.keys()[(int(sys.argv[1]) - 1)])
        else:
            add_to_series_dict(sys.argv[1])

    elif len(sys.argv) == 1:
        s_dict = load_series_dict()
        s_list = s_dict.keys()
        for s in s_list:
            print "[ {i} ] {f}".format(i=s_list.index(s) + 1, f=s)
        if len(s_list) > 0:
            str_choice = raw_input("\nEnter number:")
            choice = s_list[int(str_choice) - 1]
            play_series(s_dict, choice)
        else:
            print "No series added"

    else:
        print "Unknown arguments"
