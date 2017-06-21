"""
Contains constants and utility methods
"""

import os


def join_then_realpath(*paths):
    jp = ""
    for p in paths:
        jp = os.path.join(jp, p)
    rp = os.path.realpath(jp)
    return rp


main_drive = "C:"
alt1_drive = "F:"
user_path = "Users"

username = os.getenv("username")
file_parent_dir = join_then_realpath(os.path.dirname(__file__), os.path.pardir)

home_dir = join_then_realpath(main_drive, os.sep, user_path, username)
default_backup_dir = join_then_realpath(home_dir, "backUp")
default_backup_ext = '.gzipbak'

music_dir = join_then_realpath(alt1_drive, os.sep, user_path, username, "Music", "ytcon")
screening_dir = join_then_realpath(music_dir, "screen")

yt_amv_dir = join_then_realpath(alt1_drive, os.sep, user_path, username, "Videos", "ytAMV")
yt_dls_dir = join_then_realpath(home_dir, "Videos", "ytVids")


# TODO move to APPDATA?
logs_dir = join_then_realpath(file_parent_dir, "logs")
song_log_file = join_then_realpath(logs_dir, "prandomSongsLog.log")
removed_files_log = join_then_realpath(logs_dir, "removed_tagged_files.log")
hib_log = join_then_realpath(logs_dir, "hibLog.log")
tag_file_log = join_then_realpath(logs_dir, "tag_file.log")
vlc_hwnd_log = join_then_realpath(logs_dir, "vlc_hwnd.log")
invalidated_tag_files_log = join_then_realpath(logs_dir, "invalidated_tag_files.log")
dir_jump_file_log = join_then_realpath(logs_dir, "directoryQ.log")
tdl_log = join_then_realpath(logs_dir, "toDoListFile.log")
prev_dir_log = join_then_realpath(logs_dir, "prevDir.log")
prandom_exceptions_log = join_then_realpath(logs_dir, "prandomexceptiontags.log")
deleted_screened_log = join_then_realpath(logs_dir, "deleted_screened.log")
cleaned_fnames_log = join_then_realpath(logs_dir, "cleaned_fnames.log")
yt_dl_defaults_log = join_then_realpath(logs_dir, "yt_dl_defaults.log")
yt_dled_log = join_then_realpath(logs_dir, "yt_dled_log.log")
strack_log = join_then_realpath(logs_dir, "strack_log.log")


def ktr(u):
    from kanji_to_romaji import kanji_to_romaji
    if isinstance(u, str):
        u = u.decode('utf-8')
    print kanji_to_romaji(u)


def output_from_command(cmd_and_args):
    import subprocess
    c_ = None
    if type(cmd_and_args) == list:
        c_ = cmd_and_args

    elif type(cmd_and_args) == str:
        c_ = cmd_and_args.split()

    if c_ is None:
        raise Exception("Argument must be either list or string")

    proc = subprocess.Popen(c_, stdout=subprocess.PIPE, shell=True)
    (output, error) = proc.communicate()

    return output.strip()


def get_cmd_sizes():
    # faster than powershell -Command $host.UI.RawUI.WindowSize.Width/Height
    from struct import unpack
    from ctypes import windll, byref, create_string_buffer
    from win32console import STD_OUTPUT_HANDLE

    stdout_handle = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
    csbi = create_string_buffer(22)
    windll.kernel32.GetConsoleScreenBufferInfo(stdout_handle, byref(csbi))
    # h: short
    # H: unsigned short
    format_ = "hhhhHhhhhhh"
    left, top, right, bottom = unpack(format_, csbi.raw)[5:9]
    cmd_width = right - left + 1
    cmd_height = bottom - top + 1
    return cmd_width, cmd_height


def print_list(list_, end_range=-1, press_to_continue=True):
    """
    :param list_: list of items
    :param end_range: number of items to print
    :param press_to_continue:
        if False then print all items in list,
        if True and length of list if greater than cmd height limit then only print cmd height limit amount of items
        and require to press a key to continue printing remaining items; pressing 'q' will print remaining items
    :return:
    """

    from msvcrt import kbhit, getch
    from sys import stdout

    orig_console_color = get_console_color()

    cmd_width, cmd_height = get_cmd_sizes()

    final_print_str = ""

    if end_range == -1 or end_range > len(list_):
        end_range = len(list_)

    print "-" * (cmd_width - 1)
    try:
        for i in range(0, end_range):

            if i % 2 == 0:
                set_console_color("cyan")
            else:
                set_console_color("yellow")

            try:
                line = "[ {n} ] {item}".format(n=str(i + 1), item=str(list_[i]))
                print line
            except UnicodeEncodeError:
                line = "[ {n} ] {item}".format(n=str(i + 1), item=str(list_[i].encode("unicode_escape")))
                print line

            final_print_str += line + "\n"

            # 4 lines for: prompt, command, '-' * cmd_width, "press any key..."
            if ((i + 4) % (cmd_height - 2)) == 0 and press_to_continue:  # - 2 is to retain last line (line + offset)
                stdout.write("Press any key to continue")
                if kbhit() == 0:
                    input_char = ord(getch())
                    if input_char == ord('q') or input_char == ord('Q'):
                        press_to_continue = False
                    if input_char == 224 or input_char == 0:
                        getch()

                    stdout.write(len("Press any key to continue") * " " + "\r")

    except KeyboardInterrupt:
        set_console_color(orig_console_color)

    finally:
        set_console_color(orig_console_color)

    print "-" * (cmd_width - 1)

    final_print_str = final_print_str.strip()
    return final_print_str


def choose_from_list(list_):

    result = None
    if len(list_) > 1:
        print "Enter number:",
        try:
            choice = raw_input()
        except EOFError:  # pipes
            choice = keypress_input()

        if choice.isdigit() and len(list_) >= int(choice) > 0:
            result = list_[int(choice) - 1]

        else:
            error_alert("Error: Invalid choice. Not a valid number. Valid range 1-{er}".format(er=len(list_)))

    elif len(list_) == 1:
        result = list_[0]

    else:
        error_alert("Error: Empty list.")

    return result


def list_from_piped(stdin_output):  # TODO rename?
    import re

    if isinstance(stdin_output, list):
        stdin_output = "".join(stdin_output)

    list_item_pattern = "\[ \d+ \].+"
    number_brace_removal_pattern = "\[ \d+ \] "
    list_of_items = re.findall(list_item_pattern, stdin_output)
    piped_list_ = [re.sub(number_brace_removal_pattern, "", item) for item in list_of_items]
    if len(piped_list_) == 0:
        raise ValueError("Cannot convert piped output in to list")

    final_list = [x.replace('\"', '') for x in piped_list_]
    return final_list


def set_clipboard_data(data):
    from win32clipboard import OpenClipboard, EmptyClipboard, SetClipboardData, CloseClipboard
    from win32con import CF_TEXT
    OpenClipboard()
    EmptyClipboard()
    SetClipboardData(CF_TEXT, data)
    CloseClipboard()


def get_clipboard_data():
    from win32clipboard import OpenClipboard, CloseClipboard, GetClipboardData
    from win32con import CF_TEXT
    OpenClipboard()
    data = GetClipboardData(CF_TEXT)
    CloseClipboard()
    return data


def get_all_page_links(url):
    import requests
    from bs4 import BeautifulSoup, SoupStrainer

    url = requests.get(url).text
    soup = BeautifulSoup(url, parse_only=SoupStrainer('a'))
    links_list = soup.findAll('a')

    return links_list


def keypress_input(prompt_str=""):
    """
    Gets input from keypress until enter is pressed.
    Tries to emulates raw_input() so that it can be used with piping.
    :param prompt_str: optional string to print before getting input
    :type prompt_str: str
    """

    from msvcrt import getch
    from sys import stdout

    if len(prompt_str) > 0:
        print prompt_str

    user_input = ""
    curr_chars = []
    cursor_pos = 0

    backspace = 8
    enter = 13

    escape_code = 224
    delete = 83
    left = 75
    right = 77
    home = 71
    end = 79
    ctrl_left = 115
    ctrl_right = 116
    ctrl_home = 119
    ctrl_end = 117

    while user_input != enter:
        char_g = getch()
        user_input = ord(char_g)
        prev_len = len(curr_chars)  # track length for clearing stdout since length of curr_chars might change

        if user_input == backspace:
            if len(curr_chars) > 0 and cursor_pos <= len(curr_chars):
                cursor_pos -= 1
                curr_chars.pop(cursor_pos)

        elif user_input == escape_code:
            user_input = ord(getch())

            if user_input == delete:
                curr_chars.pop(cursor_pos)

            elif user_input == left:
                cursor_pos -= 1

            elif user_input == right:
                if cursor_pos < len(curr_chars):
                    cursor_pos += 1

            elif user_input == home:
                cursor_pos = 0

            elif user_input == end:
                cursor_pos = len(curr_chars)

            elif user_input == ctrl_home:
                curr_chars = curr_chars[cursor_pos:]
                cursor_pos = 0

            elif user_input == ctrl_end:
                curr_chars = curr_chars[:cursor_pos]
                cursor_pos = len(curr_chars)

            elif user_input == ctrl_left:
                pos_diff = cursor_pos - "".join(curr_chars[:cursor_pos]).rindex(" ")
                cursor_pos -= pos_diff

            elif user_input == ctrl_right:
                pos_diff = cursor_pos + "".join(curr_chars[cursor_pos + 1:]).index(" ") + 1
                cursor_pos = pos_diff

        elif user_input != enter:
            if cursor_pos > len(curr_chars) - 1:
                curr_chars.append(char_g)
            else:
                curr_chars.insert(cursor_pos, char_g)
            cursor_pos += 1

        # clear entire line, write contents of curr_chars, reposition cursor
        stdout.write("\r" + prev_len * " " + "\r")
        stdout.write("".join(curr_chars))
        pos_diff = len(curr_chars) - cursor_pos
        stdout.write("\b" * pos_diff)

    stdout.write("\r" + len("".join(curr_chars)) * " " + "\r")
    stdout.write("".join(curr_chars) + "\n")

    return "".join(curr_chars)


def create_backup_compressed_file(src, dest):
    import gzip
    import shutil

    if not os.path.splitext(dest)[1] == default_backup_ext:
        error_alert("Warning: destination doesn't have expected {ext} extension".format(ext=default_backup_ext))

    with open(src, 'rb') as f_in, gzip.open(dest, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)


def uncompress_backup_file(filename):
    import gzip
    import shutil

    if not os.path.splitext(filename)[1] == default_backup_ext:
        raise IOError("Not a valid backup file. {ext} extension required".format(ext=default_backup_ext))

    uncompressed_fname = filename[:-len(default_backup_ext)]
    with gzip.open(filename, 'rb') as f_in, open(uncompressed_fname, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)


def create_backup(full_filename, backup_dir=None):
    from datetime import datetime

    if not os.path.isabs(full_filename):
        full_filename = os.path.realpath(os.path.join(os.getcwd(), full_filename))

    if os.path.isfile(full_filename):
        time_format = "%b-%d-%Y@%H_%M_%f"
        filename_and_ext = os.path.split(full_filename)[1]
        filename_only, extension = os.path.splitext(filename_and_ext)

        if backup_dir is None:
            backup_dir = default_backup_dir
            backup_dir_name = os.path.join(backup_dir, filename_only)
        else:
            backup_dir_name = backup_dir

        if os.path.isdir(backup_dir_name) is False:
            print "Creating new directory: ", backup_dir_name
            os.mkdir(backup_dir_name)

        backup_full_filename = os.path.join(backup_dir_name,
                                            filename_only + "@" +
                                            str(datetime.now().strftime(time_format))[:-3] +  # -3 removes 0 padding
                                            extension + default_backup_ext)
        create_backup_compressed_file(full_filename, backup_full_filename)
    else:
        error_alert("{f} is not a valid file. No backup created.".format(f=full_filename))


def get_pid_from_arg(target):
    from psutil import Process

    if isinstance(target, int):
        pid = target

    elif isinstance(target, str):
        if target.isdigit():
            pid = int(target)
        else:
            pid = get_pid_from_name(target)

    elif isinstance(target, Process):
        pid = target.pid

    else:
        raise ValueError("argument must be either an int pid, str process name/pid, or psutil.Process object")

    return pid


def kill_proc(target):
    from os import kill
    from signal import SIGILL

    success = False
    pid = get_pid_from_arg(target)
    if pid != -1:
        kill(pid, SIGILL)
        success = True

    return success


def get_pixel(x=-1, y=-1):
    """
    Returns RGB of given x and y location.
    If no arguments given then default location will be current mouse position
    :param x: x coordinate of pixel to obtain
    :param y: y coordinate of pixel to obtain
    """

    from win32gui import GetDesktopWindow, GetWindowDC, GetPixel
    from win32api import GetCursorPos

    if x == -1 and y == -1:
        x = GetCursorPos()[0]
        y = GetCursorPos()[1]

    rgb = ()
    if x != -1 and y != -1:
        i_desktop_window_id = GetDesktopWindow()
        i_desktop_window_dc = GetWindowDC(i_desktop_window_id)  # device context
        long_colour = GetPixel(i_desktop_window_dc, x, y)
        i_colour = int(long_colour)
        rgb = (i_colour & 0xff), ((i_colour >> 8) & 0xff), ((i_colour >> 16) & 0xff)  # magical bit-shifting

    elif x == -1:
        raise ValueError("Missing 'x' coordinate")
    elif y == -1:
        raise ValueError("Missing 'y' coordinate")

    return rgb


def get_main_handle(proc_name):
    from win32gui import GetWindow, IsWindowVisible
    from win32con import GW_OWNER
    from psutil import process_iter

    pids = []
    proc_name = proc_name.lower()
    if ".exe" not in proc_name:
        proc_name = ".".join([proc_name, "exe"])
    for proc in process_iter():
        if proc.name().lower() == proc_name:
            pids.append(proc.pid)
            # don't break, multiple same proc_names are possible e.g: chrome

    handle_list = []
    for pid in pids:
        handle_list.extend(get_hwnds_for_pid(pid))

    main_handle = -1
    for h in handle_list:  # pyhandles
        if GetWindow(h, GW_OWNER) == 0 and IsWindowVisible(h):
            main_handle = h
            break

    return main_handle


def get_hwnds_for_pid(pid):
    from win32gui import IsWindowEnabled, EnumWindows
    from win32process import GetWindowThreadProcessId

    # noinspection PyShadowingNames
    def callback(hwnd, hwnds):

        if IsWindowEnabled(hwnd):
            _, found_pid = GetWindowThreadProcessId(hwnd)

            if found_pid == pid:
                hwnds.append(hwnd)

            return True

    hwnds = []
    EnumWindows(callback, hwnds)

    return hwnds


def get_pid_from_name(targ_proc_name):
    from psutil import process_iter

    result_pid = -1

    targ_proc_name = targ_proc_name.lower()
    if ".exe" not in targ_proc_name:
        targ_proc_name = ".".join([targ_proc_name, "exe"])

    for proc in process_iter():
        pname = proc.name().lower()
        if pname == targ_proc_name:
            result_pid = proc.pid
            break

    if result_pid == -1:
        error_alert("No PID found for " + targ_proc_name)

    return result_pid


def resize_window(targ_proc, width, height, relative=False):
    from win32gui import MoveWindow, GetWindowRect
    # noinspection PyUnresolvedReferences
    from pywintypes import error as pywintypes_error

    if isinstance(targ_proc, int) or (isinstance(targ_proc, str) and targ_proc.isdigit()):
        hwnd = get_hwnds_for_pid(int(targ_proc))[0]
    else:
        hwnd = get_main_handle(targ_proc)

    rect = GetWindowRect(hwnd)
    x = rect[0]
    y = rect[1]

    if relative:
        orig_width = rect[2] - rect[0]
        orig_height = rect[3] - rect[1]
        width += orig_width
        height += orig_height

    MoveWindow(hwnd, x, y, width, height, True)


def move_window(targ_proc, x, y, relative=False):
    from win32gui import MoveWindow, GetWindowRect

    # noinspection PyUnresolvedReferences
    from pywintypes import error as pywintypes_error

    if isinstance(targ_proc, int) or (isinstance(targ_proc, str) and targ_proc.isdigit()):
        hwnd = get_hwnds_for_pid(int(targ_proc))[0]
    else:
        hwnd = get_main_handle(targ_proc)

    rect = GetWindowRect(hwnd)

    width = rect[2] - rect[0]
    height = rect[3] - rect[1]

    if relative:
        x += rect[0]
        y += rect[1]

    MoveWindow(hwnd, x, y, width, height, True)


def keyboard_type(keystrokes, targ_proc=None):
    """
    Alt=%, CTRL=^, Shift=+
    Shift + F10= Context Menu/ Menu Key
    ~ 	{~} 	send a tilde (~)
    ! 	{!} 	send an exclamation point (!)
    ^ 	{^} 	send a caret (^)
    + 	{+} 	send a plus sign (+)
    Alt 	{ALT} 	send an Alt keystroke
    Backspace 	{BACKSPACE} 	send a Backspace keystroke
    Clear 	{CLEAR} 	Clear the field
    Delete 	{DELETE} 	send a Delete keystroke
    Down Arrow 	{DOWN} 	send a Down Arrow keystroke
    End 	{END} 	send an End keystroke
    Enter 	{ENTER} 	send an Enter keystroke
    Escape 	{ESCAPE} 	send an Esc keystroke
    F1 through F16 	{F1} through {F16} 	send the appropriate Function key
    Page Down 	{PGDN} 	send a Page Down keystroke
    Space 	{SPACE} 	send a Spacebar keystroke
    Tab 	{TAB} 	send a Tab keystroke

    {Ctrl+Esc} send Windows keystroke
    {key number} repeat `key` `number` of times
        e.g: {h 10} press h 10 times.

    :param keystrokes: keystrokes to send
    :type keystrokes: str
    :param targ_proc: process to send the keystrokes to
    :type targ_proc: int or str or psutil.Process
    """

    from win32com import client

    dict_mapping = {"~": "{~}", "!": "{!}", "+": "{+}", "(": "{(}", ")": "{)}", "%": "{%}"}
    for key in dict_mapping.keys():
        keystrokes = keystrokes.replace(key, dict_mapping[key])

    shell = client.Dispatch("WScript.Shell")

    if targ_proc is not None:
        pid = get_pid_from_arg(targ_proc)
        shell.AppActivate(pid)

    shell.SendKeys(keystrokes)

    # media keys ...
    # vk_media_next_track = 0xB0
    # hwcode = win32api.MapVirtualKey(vk_media_next_track, 0)
    # win32api.keybd_event(vk_media_next_track, hwcode)


def get_console_color():
    """
    Returns the console color resulting from
        foreground color | foreground intensity | background color | background intensity
        '|' is bitwise-or
    """
    from ctypes import windll, Structure, c_short, c_ushort, byref
    from win32console import STD_OUTPUT_HANDLE

    class ConsoleScreenBufferInfo(Structure):
        class Coord(Structure):
            _fields_ = [
                ("X", c_short),
                ("Y", c_short)]

        class SmallRect(Structure):
            _fields_ = [
                ("Left", c_short),
                ("Top", c_short),
                ("Right", c_short),
                ("Bottom", c_short)]

        _fields_ = [
            ("dwSize", Coord),
            ("dwCursorPosition", Coord),
            ("wAttributes", c_ushort),
            ("srWindow", SmallRect),
            ("dwMaximumWindowSize", Coord)
        ]

    csbi = ConsoleScreenBufferInfo()
    stdout_handle = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)

    windll.kernel32.GetConsoleScreenBufferInfo(stdout_handle, byref(csbi))

    return csbi.wAttributes


def set_console_color(color):
    """
    Sets the foreground and background colors of the console screen
    Color is a combination/bitwise-or of foreground and background color, and intensities.
    :param color:
            int result of already bitwise-or(ed) fg & bg color, and intensities
                e.g: 142
            str will only change foreground color. Will match to a listed color in color_choices dict
                e.g: set_console_color("red") will match FOREGROUND_RED
            tuple of integer colors
                e.g (0x0002, 0x0008, 0x0070, 0x0080) which is
                (FOREGROUND_GREEN, FOREGROUND_INTENSITY, BACKGROUND_GREY, BACKGROUND_INTENSITY)
    """
    color_choices = {
        "FOREGROUND_BLACK": 0x0000,
        "FOREGROUND_BLUE": 0x0001,
        "FOREGROUND_GREEN": 0x0002,
        "FOREGROUND_CYAN": 0x0003,
        "FOREGROUND_RED": 0x0004,
        "FOREGROUND_MAGENTA": 0x0005,
        "FOREGROUND_YELLOW": 0x0006,
        "FOREGROUND_GREY": 0x0007,
        "FOREGROUND_INTENSITY": 0x0008,

        "BACKGROUND_BLACK": 0x0000,
        "BACKGROUND_BLUE": 0x0010,
        "BACKGROUND_GREEN": 0x0020,
        "BACKGROUND_CYAN": 0x0030,
        "BACKGROUND_RED": 0x0040,
        "BACKGROUND_MAGENTA": 0x0050,
        "BACKGROUND_YELLOW": 0x0060,
        "BACKGROUND_GREY": 0x0070,
        "BACKGROUND_INTENSITY": 0x0080
    }

    from win32console import STD_OUTPUT_HANDLE
    from ctypes import windll

    stdout_handle = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)

    if isinstance(color, tuple):
        temp_tuple = tuple(color)
        color = 0
        for c in temp_tuple:
            color |= c

    elif isinstance(color, str):
        try:
            if "FOREGROUND" not in color:
                color = color_choices["".join(["FOREGROUND_", color.upper()])]  # assuming foreground only for str
        except KeyError:
            err_msg = "".join(["Invalid foreground color: ", color])
            error_alert(err_msg)

    if not isinstance(color, int):
        raise ValueError("color must be an integer or string")

    windll.kernel32.SetConsoleTextAttribute(stdout_handle, color)


def print_colored(text, color):
    orig_color = get_console_color()
    set_console_color(color)
    try:
        print text,
    except (UnicodeDecodeError, UnicodeEncodeError):
        set_console_color(orig_color)
    finally:
        set_console_color(orig_color)


def error_alert(msg):
    print_colored(msg, "red")


def get_pid_from_handle(handle):
    from psutil import process_iter
    excluded_processes = ["audiodg.exe", "system.exe", "svchost.exe",
                          "system idle process.exe", "system", "system idle process"]

    result_pid = -1

    for proc in process_iter():
        if proc.name().lower() not in excluded_processes and \
                        handle in get_hwnds_for_pid(get_pid_from_name(proc.name())):
            result_pid = proc.pid
            break

    return result_pid


def move_mouse(x, y):
    from mouse_macro import move

    try:
        x = int(x)
        y = int(y)
    except ValueError:
        raise ValueError("Invalid arguments. x and y must be either an int or str that is a digit.")

    move(x, y)


def write_inline(w_str):
    from sys import stdout
    w_str = str(w_str)
    cmd_width = get_cmd_sizes()[0]
    stdout.write("\r" + (" " * cmd_width) + "\r")  # clear entire line
    stdout.write(w_str)
    stdout.flush()


def get_media_player_path():
    vlc_exe_path = os.path.join(os.getenv("PROGRAMFILES"), "VideoLAN", "VLC", "vlc.exe")
    if not os.path.isfile(vlc_exe_path):
        vlc_exe_path = os.path.join(os.getenv("PROGRAMFILES(x86)"), "VideoLAN", "VLC", "vlc.exe")
    if not os.path.isfile(vlc_exe_path):
        raise IOError("VLC player not found")

    return vlc_exe_path


def self_validate_globals():
    root_dir_list = [music_dir, screening_dir, default_backup_dir, yt_amv_dir, yt_dls_dir]

    root_f_list = [song_log_file, removed_files_log, hib_log, tag_file_log, vlc_hwnd_log, invalidated_tag_files_log,
                   dir_jump_file_log, tdl_log, prev_dir_log, prandom_exceptions_log, deleted_screened_log,
                   cleaned_fnames_log, yt_dl_defaults_log, strack_log]

    for rd in root_dir_list:
        try:
            assert os.path.isdir(rd)
        except AssertionError:
            raise AssertionError(rd + " is not a directory")

    for rf in root_f_list:
        try:
            assert os.path.isfile(rf)
        except AssertionError:
            raise AssertionError(rf + " is not a file")


self_validate_globals()
