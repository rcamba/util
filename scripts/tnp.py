import os
import sys
import json
import time
import psutil
import subprocess

import win32gui
from root import strack_log, keyboard_type, get_hwnds_for_pid, print_list, choose_from_list, get_media_player_path


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


def get_vlc_pid():
    proc_id = -1
    for proc in psutil.process_iter():
        if proc.name() == "vlc.exe":
            proc_id = proc.pid
    return proc_id


def play_series(series_dict, series_path):
    def input_prompt():
        return raw_input("[{next}] to play next file or [{quit}] to quit program\n".format(
            next=next_key_press, quit=quit_key_press)).lower()

    next_key_press = "n"
    quit_key_press = "q"
    user_input = next_key_press
    valid_inputs = [next_key_press, quit_key_press]
    first_run = True
    proc_pid = get_vlc_pid()
    vlc_opts = "--one-instance"
    while user_input != quit_key_press and series_path in series_dict:
        if user_input == next_key_press:
            play_now = series_dict[series_path].pop(0)
            print play_now
            if first_run:
                if proc_pid == -1:  # vlc not yet open
                    proc = subprocess.Popen([get_media_player_path(), vlc_opts,
                                             os.path.join(series_path, play_now)])
                    proc_pid = proc.pid

                while len(get_hwnds_for_pid(proc_pid)) == 0:
                    time.sleep(0.5)

                keyboard_type("f", proc_pid)  # fullscreen

            else:
                subprocess.Popen([get_media_player_path(), vlc_opts,
                                  os.path.join(series_path, play_now)])
                time.sleep(0.5)  # wait for fname to be added to queue

                # noinspection PyUnboundLocalVariable
                win32gui.SetForegroundWindow(get_hwnds_for_pid(proc.pid)[0])
                keyboard_type("n", proc_pid)

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
        if len(s_list) > 0:
            print_list(s_list)
            choice = choose_from_list(s_list)
            play_series(s_dict, choice)
        else:
            print "No series added"

    else:
        print "Unknown arguments"
