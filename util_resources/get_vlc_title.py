from win32gui import GetWindowText, IsWindowEnabled, EnumWindows
from win32process import GetWindowThreadProcessId
from psutil import process_iter
try:
    from simplejson import load
except ImportError:
    from json import load

from root import vlc_hwnd_log, set_clipboard_data, song_log_file
from os import path
from search_tags import search_tags_for_file


def get_hwnds_for_pid(pid):
    def callback(hwnd, hwnds_):

        if IsWindowEnabled(hwnd):
            _, found_pid = GetWindowThreadProcessId(hwnd)

            if found_pid == pid:
                hwnds_.append(hwnd)

        return True

    hwnds = []
    EnumWindows(callback, hwnds)

    return hwnds


def get_vlc_hwnd():

    """
    Check if vlc_hwnd stored in vlc_hwnd_log file is still for vlc
    if it is then use it
    otherwise try to find vlc hwnd
        finding hwnd requires process ID
        find PID by iterating through all active processes looking for vlc
    """

    vlc_hwnd = -1

    f = open(vlc_hwnd_log, 'r')
    vlc_num_from_file = f.read()
    f.close()

    if (vlc_num_from_file.isdigit() and
            "media player" in GetWindowText(int(vlc_num_from_file))):
        vlc_hwnd = int(vlc_num_from_file)

    else:
        vlc_pid = -1

        for proc in process_iter():
            if proc.name() == "vlc.exe":
                vlc_pid = proc.pid
                break

        hwnd_list = get_hwnds_for_pid(vlc_pid)

        for hwnd in hwnd_list:
            if "VLC media player" in GetWindowText(hwnd):
                vlc_hwnd = hwnd
                f = open(vlc_hwnd_log, "w+")
                f.write(str(hwnd))
                f.close()

    return vlc_hwnd


def _get_vlc_title(vlc_hwnd):

    vlc_title = title_from_hwnd(vlc_hwnd)
    return vlc_title


def path_from_hwnd(vlc_hwnd):

    # VLC Tools -> Preferences -> Show "All" Settings ->
    # Input/Codecs -> Change title according to current media =$F
    # Displays file path to current media in VLC window text

    window_title = GetWindowText(vlc_hwnd)

    translation_dict = {
        " - VLC media player": "",
        "file:///": "",
        "%20": " ",
        "%28": "(",
        "%29": ")",
        "%5B": "[",
        "%5D": "]",
        "%27": "'",
        "%40": "@",
        "%2B": "+",
        "%2C": ",",
    }

    for key in translation_dict.keys():
        window_title = window_title.replace(key, translation_dict[key])
    file_path = path.normpath(window_title)

    return file_path.lower()


def title_from_hwnd(vlc_hwnd):

    file_path = path_from_hwnd(vlc_hwnd)
    title = path.split(file_path)[1]
    return title


def get_song_play_count(song_filename):
    with open(song_log_file) as reader:
        song_log_dict = load(reader)
    song_filename = song_filename.replace("\"", "").strip()
    if song_filename in song_log_dict:
        play_count = song_log_dict[song_filename]["play_count"]
    else:
        play_count = 0

    return play_count


def get_vlc_title():

    vlc_hwnd = get_vlc_hwnd()
    vlc_title = _get_vlc_title(vlc_hwnd)
    fp = path_from_hwnd(vlc_hwnd)
    quoted_fp = "\"" + fp + "\""

    print "+ Currently playing:"
    print vlc_title
    print quoted_fp
    set_clipboard_data(quoted_fp)
    tags = search_tags_for_file(fp)
    if len(tags) == 0:
        print "No tags"
    else:
        print "Tags:", ", ".join(tags)
    print get_song_play_count(fp), "play(s)"

    return fp


if __name__ == "__main__":
    get_vlc_title()
