"""
Contains all constants and some utility methods
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

# Files
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

# Variables
MAX_WAIT_TIME = 30  # seconds

# Utility methods


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

    out = output_from_command("powershell -Command $host.UI.RawUI.WindowSize.Height")
    cmd_height = int(out) - 1  # -1 for prompt ("Press any key to continue")

    out = output_from_command("powershell -Command $host.UI.RawUI.WindowSize.Width")
    cmd_width = int(out)

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
                line = "[" + " " + str(i + 1) + " " + "] " + str(list_[i])
                print line
            except UnicodeEncodeError:
                line = "[" + " " + str(i + 1) + " " + "] " + list_[i].encode("unicode_escape")
                print line

            final_print_str += line + "\n"

            if ((i + 1) % cmd_height) == 0 and press_to_continue:
                stdout.write("Press any key to continue")
                if kbhit() == 0:
                    input_char = ord(getch())
                    if input_char == ord('q') or input_char == ord('Q'):
                        press_to_continue = False
                    if input_char == 224 or input_char == 0:
                        getch()

                    stdout.write(len("Press any key to continue") * "\b")
                    stdout.write(len("Press any key to continue") * " ")
                    stdout.write(len("Press any key to continue") * "\b")

    except KeyboardInterrupt:
        set_console_color(orig_console_color)

    finally:
        set_console_color(orig_console_color)

    print "-" * (cmd_width - 1)

    final_print_str = final_print_str.strip()
    return final_print_str


def choose_from_list(list_):
    from sys import exit as sys_exit

    result = -1
    if len(list_) > 1:
        print "Enter number of desired result: ",
        try:
            choice = raw_input()
        except EOFError:  # pipes
            choice = key_press_input()

        if choice.isdigit() and len(list_) >= int(choice) > 0:
            result = int(choice) - 1

        else:
            error_alert("Error: Invalid choice. Not a valid number. Valid range 1-{er}".format(er=len(list_)))
            sys_exit(1)

    elif len(list_) == 1:
        result = 0

    else:
        error_alert("Error: Empty list.")

    return list_[result]


def list_from_piped(stdin_output):
    import re

    if isinstance(stdin_output, list):
        stdin_output = "".join(stdin_output)

    list_item_pattern = "\[ \d+ \].+"
    number_brace_removal_pattern = "\[ \d+ \] "
    list_of_items = re.findall(list_item_pattern, stdin_output)
    piped_list_ = [re.sub(number_brace_removal_pattern, "", item) for item in list_of_items]
    if len(piped_list_) == 0:
        error_alert("Cannot convert piped output in to list", raise_exception=True)

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
    # user-agent?
    url = requests.get(url).text

    from bs4 import BeautifulSoup, SoupStrainer
    resultsList = BeautifulSoup(url, parse_only=SoupStrainer('a'))
    resultsList = resultsList.findAll('a')

    return resultsList


def prompt():
    from sys import stdout
    from os import system
    system("echo %CD%")
    stdout.write(">>>")


def key_press_input(prompt_str=""):
    """
    Gets input from keypress until enter is pressed.
    Tries to emulates raw_input() ; insert/overwrite always on
    For use with pipes
    """

    if len(prompt_str) > 0:
        print prompt_str

    def clear(length=1):
        stdout.write("\b" * length)  # stdout cursor move back by length
        stdout.write(" " * length)  # display clearing of character(s)
        stdout.write("\b" * length)  # get rid of " " moving cursor forward

    from msvcrt import kbhit, getch
    from sys import stdout

    user_input = ""
    result = []
    cursor_pos = 0

    while user_input != 13:
        char_g = getch()
        user_input = ord(char_g)

        if user_input == 13:
            clear(len("".join(result)))
            stdout.write("".join(result) + "\n")

        elif user_input == 8:
            if len(result) > 0 and cursor_pos <= len(result):
                clear(len(result))
                cursor_pos -= 1
                result.pop("".join(result).rindex(result[cursor_pos]))

                stdout.write("".join(result))
                stdout.write("\b" * (len(result) - cursor_pos))

        elif user_input == 224:
            user_input = ord(getch())

            if user_input == 75:  # left
                cursor_pos -= 1
                stdout.write("\b")

            elif user_input == 77:  # right
                if cursor_pos < len(result):
                    stdout.write(result[cursor_pos])
                else:
                    stdout.write(" ")
                cursor_pos += 1

            elif user_input == 119:  # ctrl+home
                clear(len(result))

                result = result[cursor_pos:]

                stdout.write("".join(result))  # let cursor remain at end
                cursor_pos = len(result)

            elif user_input == 117:  # ctrl+end
                clear(len(result))
                result = result[:cursor_pos]

                stdout.write("".join(result))
                cursor_pos = len(result)

            elif user_input == 115:  # ctrl+left

                diff_pos = cursor_pos - "".join(result).rindex(" ")
                stdout.write("\b" * diff_pos)
                cursor_pos = cursor_pos - diff_pos

            elif user_input == 116:  # ctrl + right
                pass

        else:

            stdout.write(char_g)
            result.insert(cursor_pos, char_g)
            cursor_pos += 1

    return "".join(result)


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
        error_alert("Not a valid backup file. {ext} extension required".format(ext=default_backup_ext),
                    raise_exception=True, err_class=IOError)

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


def kill_proc(proc_name="", pid=-1):
    from psutil import pids, Process
    from os import kill
    from signal import SIGILL
    from string import lower

    success = -1
    if len(proc_name) > 0 or pid != -1:

        if proc_name.isdigit():
            pid = int(proc_name)
            kill(pid, SIGILL)
            success = 1

        elif pid == -1:
            if ".exe" not in proc_name:
                proc_name = ".".join([lower(proc_name), "exe"])
            for procPID in pids():
                try:
                    if lower(Process(procPID).name) == proc_name:
                        kill(procPID, SIGILL)
                        success = 1

                except Exception, e:
                    print e.message

        else:
            error_alert("Unable to find process.")
    else:
        error_alert("Missing processName or pid parameter")

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
    from sys import exit as sys_exit

    if x == -1 and y == -1:
        x = GetCursorPos()[0]
        y = GetCursorPos()[1]

    if x != -1 and y != -1:
        i_desktop_window_id = GetDesktopWindow()
        i_desktop_window_dc = GetWindowDC(i_desktop_window_id)  # device context
        try:
            long_colour = GetPixel(i_desktop_window_dc, x, y)
        except:
            print "Coordinates ", x, ",", y, "out of screen size"
            sys_exit(1)

        i_colour = int(long_colour)

    elif x == -1:
        print "Missing 'y' coordinate"
        sys_exit(1)
    elif y == -1:
        print "Missing 'x' coordinate"
        sys_exit(1)

    return (i_colour & 0xff), ((i_colour >> 8) & 0xff), ((i_colour >> 16) & 0xff)  # magical bit-shifting


def get_hwnds_for_pid(pid):
    from win32gui import IsWindowEnabled, EnumWindows
    from win32process import GetWindowThreadProcessId

    def callback(hwnd, hwnds):

        if IsWindowEnabled(hwnd):
            _, found_pid = GetWindowThreadProcessId(hwnd)

            if found_pid == pid:
                hwnds.append(hwnd)

        return True

    hwnds = []
    EnumWindows(callback, hwnds)

    return hwnds


def get_proc_pid(target):
    """
            Returns PID of given process name argument
    """
    from psutil import pids, Process
    from string import lower
    from sys import exit as sys_exit

    EXCLUDED_PROCESSES = ["audiodg.exe", "soffice.bin.exe", "system.exe",
                          "svchost.exe", "system idle process.exe", "system", "system idle process"]

    result_pid = -9000
    target = lower(target)

    if ".exe" not in target:
        target = ".".join([target, "exe"])

    if type(target) == str and target not in EXCLUDED_PROCESSES:

        for PID in pids():

            if lower(Process(PID).name) not in EXCLUDED_PROCESSES and lower(Process(PID).name) == target:
                result_pid = PID
                break

        if result_pid == -9000:
            error_alert("No PID found for " + target)
            error_alert("Terminating script")
            sys_exit(1)

    else:
        error_alert("Passed argument: {t} is invalid. Must be string type argument and not an excluded process".
                    format(t=target))

    return result_pid


def resize_window(width, height, proc_name="cmd", pid=-1):
    from win32gui import MoveWindow, GetWindowRect

    if pid == -1:
        proc_pid = get_proc_pid(proc_name)
    else:
        proc_pid = pid

    hwnd_list = get_hwnds_for_pid(proc_pid)
    # hwnd=hwndList[0]
    for hwnd in hwnd_list:

        win_rect = GetWindowRect(hwnd)
        x = win_rect[0]
        y = win_rect[1]

        MoveWindow(hwnd, x, y, width, height, True)


def move_window(x, y, proc_name="", pid=-1, hwnd=-1, width=-1, height=-1):
    from win32gui import MoveWindow, GetWindowRect
    from sys import exit as sys_exit
    from pywintypes import error as pywintypesError

    if type(proc_name) == int:
        process_pid = proc_name

    elif len(proc_name) == 0 and pid == -1:
        error_alert("Must pass at least one argument, either process name or PID")
        sys_exit(1)

    elif len(proc_name) > 0 and pid == -1:  # case for just the process name passed

        if proc_name.isdigit():  # case for accidentally pid as first argument
            process_pid = int(proc_name)

        else:
            process_pid = get_proc_pid(proc_name)

    elif len(proc_name) == 0 and pid != -1:
        process_pid = pid

    else:
        error_alert("Cannot have both process name and PID argument passed.")
        sys_exit(1)

    hwnd_list = get_hwnds_for_pid(process_pid)

    hwnd = hwnd_list[0]

    if width == -1 and height == -1:

        try:
            rect = GetWindowRect(hwnd)  # get window sizes to keep the window sizes similar when moving them
            width = rect[2] - rect[0]
            height = rect[3] - rect[1]

        except pywintypesError:
            print "Invalid window handle."
            sys_exit(1)

    MoveWindow(hwnd, x, y, width, height, True)


def get_handle(proc_name):
    try:
        return get_hwnds_for_pid(get_proc_pid(proc_name))[0]
    except IndexError:
        print "No handle found"
        return -1


def keyboard_type(key_char, targ_prog_name=""):
    from win32com import client

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
    """

    shell = client.Dispatch("WScript.Shell")
    if len(targ_prog_name) > 0:
        shell.AppActivate(targ_prog_name)
    dict_mapping = {"~": "{~}", "!": "{!}", "+": "{+}", "(": "{(}", ")": "{)}"}

    for key in dict_mapping.keys():
        key_char = key_char.replace(key, dict_mapping[key])

    shell.SendKeys(key_char)


def get_console_color():
    from cmd_coloring import get_console_color as gcc
    return gcc()


def set_console_color(color):
    from cmd_coloring import set_console_color as scc, COLOR_CHOICES

    if type(color) == int:
        scc(color)

    else:
        try:
            scc(COLOR_CHOICES["".join(["FOREGROUND_", color.upper()])])
        except KeyError:
            err_msg = "".join(["Invalid foreground color: ", color])
            error_alert(err_msg)


def print_colored(text, color):
    orig_color = get_console_color()
    set_console_color(color)
    print text
    set_console_color(orig_color)


def error_alert(msg="", raise_exception=False, err_class=None):
    # if colouring fails resort ignore it and just print msg
    orig_cmd_fg_color = get_console_color()
    set_console_color("red")

    try:
        if raise_exception:
            if err_class is not None:
                raise err_class(msg)
            else:
                raise Exception(msg)
        else:
            print msg

        set_console_color(orig_cmd_fg_color)

    except:
        set_console_color(orig_cmd_fg_color)
        raise

    return msg


def take_screenshot(prog_name=""):

    from win32gui import GetDesktopWindow, GetWindowRect, GetWindowDC, ReleaseDC, GetWindowText, GetForegroundWindow
    from win32ui import CreateDCFromHandle, CreateBitmap
    from win32con import SRCCOPY
    from datetime import datetime
    from psutil import Process

    # appName=GetWindowText(GetForegroundWindow())
    if len(prog_name) == 0:
        prog_name = Process(get_pid_from_handle(GetForegroundWindow())).name

    windows_handle = GetDesktopWindow()

    rect = GetWindowRect(windows_handle)
    width = rect[2] - rect[0]
    height = rect[3] - rect[1]
    left = rect[0]  # win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
    top = rect[1]  # win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)

    hwindc = GetWindowDC(windows_handle)
    srcdc = CreateDCFromHandle(hwindc)
    memdc = srcdc.CreateCompatibleDC()
    data_bitmap = CreateBitmap()

    data_bitmap.CreateCompatibleBitmap(srcdc, width, height)
    memdc.SelectObject(data_bitmap)
    memdc.BitBlt((0, 0), (width, height), srcdc, (left, top), SRCCOPY)
    fname = "".join(["SS_", prog_name, "_", str(datetime.now().strftime("%b-%d-%Y@%H_%M_%S")).strip(), ".bmp"])
    print "Saved screenshot as :", fname
    data_bitmap.SaveBitmapFile(memdc, fname)

    srcdc.DeleteDC()
    memdc.DeleteDC()
    ReleaseDC(windows_handle, hwindc)

    return fname


def get_pid_from_handle(handle):
    from psutil import pids, Process
    from string import lower
    EXCLUDED_PROCESSES = ["audiodg.exe", "system.exe", "svchost.exe",
                          "system idle process.exe", "system", "system idle process"]

    result_pid = -1

    for pid in pids():
        if lower(Process(pid).name) not in EXCLUDED_PROCESSES and \
                        handle in get_hwnds_for_pid(get_proc_pid(Process(pid).name)):
            result_pid = pid
            break

    return result_pid


def crop_img(img_fname, crop_box):
    import Image

    img = Image.open(img_fname)
    extension = img_fname[img_fname.rindex('.'):]
    frame = img.crop(crop_box)
    save_filename = "".join(["cropped_", img_fname, extension])
    frame.save(save_filename)

    return save_filename


def move_mouse(x, y):
    from mouse_macro import move

    try:
        x = int(x)
        y = int(y)
    except ValueError:
        error_alert("Invalid arguments. Must be integer")

    move(x, y)


def stdout_write(w_str):
    import sys
    w_str = str(w_str)
    sys.stdout.write("\b" * len(w_str))
    sys.stdout.write(w_str)
    sys.stdout.flush()


def self_validate_globals():
    root_dir_list = [music_dir, screening_dir, default_backup_dir, yt_amv_dir, yt_dls_dir]

    root_f_list = [song_log_file, removed_files_log, hib_log, tag_file_log, vlc_hwnd_log, invalidated_tag_files_log,
                   dir_jump_file_log, tdl_log, prev_dir_log, prandom_exceptions_log, deleted_screened_log,
                   cleaned_fnames_log, yt_dl_defaults_log]

    for rd in root_dir_list:
        try:
            assert os.path.isdir(rd)
        except AssertionError:
            # error_alert
            raise AssertionError(rd + " is not a directory")

    for rf in root_f_list:
        try:
            assert os.path.isfile(rf)
        except AssertionError:
            # error_alert
            raise AssertionError(rf + " is not a file")


self_validate_globals()
