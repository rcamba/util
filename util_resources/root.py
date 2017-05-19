"""
Contains all constants and some utility methods
"""

from os import getenv, path, sep
parent_dir = path.join(path.dirname(__file__), path.pardir)
username = getenv("username")

main_drive = "C:"
alt1_drive = "F:"
user_path = "Users"

home_dir = path.join(main_drive, sep, user_path, username)
backup_dir = path.join(home_dir, "backUp")

music_dir = path.join(alt1_drive, sep, user_path, username, "Music", "ytcon")
screening_dir = path.join(music_dir, "screen")

yt_amv_dir = path.join(alt1_drive, sep, user_path, username,  "Videos", "ytAMV")
yt_dls_dir = path.join(home_dir, "Videos", "ytVids")

tag_files_log_dir = path.join(parent_dir, "logs", "tagFilesLog")

# Files
# TODO move to APPDATA?
song_log_file = path.join(parent_dir, "logs", "prandomSongsLog.log")
removed_files_log = path.join(parent_dir, "logs", "removedFilesLog.log")
hib_log = path.join(parent_dir, "logs", "hibLog.log")
tag_file_log = path.join(parent_dir, "logs", "tagFile.log")
vlc_hwnd_log = path.join(parent_dir, "logs", "vlc_hwnd.log")
deleted_tag_files_log = path.join(parent_dir, "logs", "deletedTagFiles.log")
dir_jump_file_log = path.join(parent_dir, "logs", "directoryQ.log")
tdl_log = path.join(parent_dir, "logs", "toDoListFile.log")
prev_dir_log = path.join(parent_dir, "logs", "prevDir.log")
prandom_exceptions_log = path.join(parent_dir, "logs", "prandomexceptiontags.log")
deleted_screened_log = path.join(parent_dir, "logs", "deletedScreenedLog.log")
cleaned_fnames_log = path.join(parent_dir, "logs", "cleaned_fnames.log")

# Variables
MAX_WAIT_TIME = 30  # seconds

# Utility methods


def switch_board(args, valid_switches=None):
    from string import lower
    from inspect import stack, getmodule, getmodulename
    from sys import exit as sys_exit
    if valid_switches is None:

        frame = stack()[1]
        try:
            module = getmodule(frame[0]).__file__
            import_file = getmodulename(module)
            valid_switches = __import__(import_file).__dict__.get("AVAILABLE_SWITCHES")
            # AVAILABLE SWITCHES CAN'T BE INSIDE "If __name__==__main__" BLOCK

            if valid_switches is None:
                print "No valid switches found. Terminating script."
                sys_exit(1)

        except TypeError:
            print "Module of ", frame[0], " not found"
            sys_exit(1)

        except AttributeError:
            valid_switches = [arg.replace("-", "") for arg in args]

    switch_list = []
    if type(args) == list:

        for i in range(len(args) - 1, -1, -1):

            if "-" in args[i][0]:
                switch = args[i].replace("-", "")
                if len(switch) > 0:

                    if ":" in switch:
                        token = switch.split(":")
                        if token[0] in valid_switches:
                            switch_list.append((token[0], token[1]))
                        else:
                            print token[0], ": not a valid switch"
                            sys_exit(1)

                    elif lower(switch) in valid_switches:
                        switch_list.append(lower(switch))
                    else:
                        print "Invalid switch: ", switch
                        print "Terminating script."
                        sys_exit(1)
                args.remove(args[i])

        # standard/ normalize slashes for file accesses
            elif "/" in args[i]:
                args[i] = args[i].replace("/", "\\")

    else:
        print "Not a list"

    return switch_list


def switch_parser(args, valid_switches=None):  # returns dict, will replace switch_board
    from inspect import stack, getmodule, getmodulename
    from sys import exit as sys_exit

    if valid_switches is None:
        frame = stack()[1]
        try:
            module = getmodule(frame[0]).__file__
            import_file = getmodulename(module)
            valid_switches = __import__(import_file).__dict__.get("AVAILABLE_SWITCHES")
            # AVAILABLE SWITCHES CAN'T BE INSIDE "If __name__==__main__" BLOCK
            if valid_switches is None:
                print "No valid switches found. Terminating script."
                sys_exit(1)

        except TypeError:
            print "Module of ", frame[0], " not found"
            sys_exit(1)

        except AttributeError:
            valid_switches = [arg.replace("-", "") for arg in args]

    switch_dict = {}
    for arg in args[:]:
        if arg[0] == '-':

            token = arg.split(':')

            if token[0][1:] in valid_switches:
                if len(token) == 1:
                    switch_dict[token[0][1:]] = ''

                elif len(token) == 2:
                    switch_dict[token[0][1:]] = token[1]

                else:
                    switch_dict[token[0][1:]] = " ".join([token[1:]])

            else:
                print "\nInvalid switch: ", token[0][1:]
                print "Valid switches: ", valid_switches
                sys_exit(1)

            args.remove(arg)

    return switch_dict


def list_from_piped():
    pass  # get list from piped print_numbered_list/ print_list


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


def print_list(list_, end_range=-1, scheme="full", press_to_continue=True):
    """

    :param list_: list of items
    :param end_range: number of items to print
    :param scheme: printing scheme determining console color, border, row item symbols
    :param press_to_continue:
        if False then print all items in list,
        if True and length of list if greater than cmd height limit then only print cmd height limit amount of items
        and require to press a key to continue printing remaining items
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

    # noinspection PyDictCreation
    schemes_dict = {}

    schemes_dict["full"] = {
        "print_border": "-" * (cmd_width - 1),
        "console_colors": [3, 6],
        "char_symbols": ['+', '-', '!']
    }

    schemes_dict["border_only"] = {
        "print_border": "-" * (cmd_width - 1),
        "console_colors": [orig_console_color, orig_console_color],
        "char_symbols": ['', '', '']
    }

    schemes_dict["none"] = {
        "print_border": "",
        "console_colors": [orig_console_color, orig_console_color],
        "char_symbols": ['', '', '']
    }

    if len(schemes_dict[scheme]["print_border"]) > 0:
        print schemes_dict[scheme]["print_border"]

    try:
        for i in range(0, end_range):

            if i % 2 == 0:
                set_console_color(schemes_dict[scheme]["console_colors"][0])
            else:
                set_console_color(schemes_dict[scheme]["console_colors"][1])

            char_symbols = schemes_dict[scheme]["char_symbols"]

            c_symbol = char_symbols[i % len(char_symbols)]
            if scheme == "none" or scheme == "border_only":
                line = str(list_[i])

            else:
                line = "[" + c_symbol + " " + str(i + 1) + " " + c_symbol + "] " + \
                    str(list_[i]) + " [" + (c_symbol + c_symbol) + "]"
            print line
            final_print_str += line + "\n"

            if ((i + 1) % cmd_height) == 0 and press_to_continue:
                stdout.write("Press any key to continue")
                if kbhit() == 0:
                    input_char = ord(getch())
                    if input_char == 224 or input_char == 0:
                        getch()

                    stdout.write(len("Press any key to continue") * "\b")

    except KeyboardInterrupt:
        set_console_color(orig_console_color)

    finally:
        set_console_color(orig_console_color)

    if len(schemes_dict[scheme]["print_border"]) > 0:
        print schemes_dict[scheme]["print_border"]

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
            error_alert("Error: Invalid choice. Choice was not a valid number.")
            sys_exit(1)

    elif len(list_) == 1:
        result = 0

    else:
        error_alert("Error: Empty list.")

    return list_[result]


def piped_list(stdin_output):
    from re import findall
    try:

        piped_list_ = findall("\".+\"", stdin_output)
        final_list = [x.replace('\"', '') for x in piped_list_]

    except Exception, e:
        error_alert(str(e))
        error_alert("Cannot convert: " + stdin_output + "from pipes in to list")
        final_list = []

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


def add_member(original_obj, function=None, man_attrib=""):

    # function must contain a function call that can be applied to originalObject

    class Metamorph:

        def __init__(self, original_obj_, func_):
            self.object = original_obj_

            if len(man_attrib) > 0:
                self.attribute = man_attrib
            elif len(func_.__name__) > 0:
                try:
                    self.attribute = func_(original_obj_)
                except:
                    self.attribute = None
                    print "Failed to set", func_, "for: ", original_obj_
                    raise WindowsError  # TODO: CREATE OWN ERROR EXCEPTION
            else:
                print "Missing function or manual attribute parameter."

        def get_object(self):
            return self.object

        def get_attribute(self):
            return self.attribute

        def __str__(self):
            return original_obj.__str__()

    result = Metamorph(original_obj, function)

    return result


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


def file_search(target_file, top_lvl="C:\\Users\\Kevin\\", strict=True):
    from string import lower

    from os import path, listdir

    EXCLUDED_FOLDERS = [
        path.join(home_dir, "application data"),
        path.join(home_dir, "cookies"),
        path.join(home_dir, "local settings"),
        path.join(home_dir, "nethood"),
        path.join(home_dir, "printhood"),
        path.join(home_dir, "recent"),
        path.join(home_dir, "sendto"),
        path.join(home_dir, "start menu"),
        path.join(home_dir, "templates"),
        path.join(home_dir, "appdata", "local", "temporary internet files"),
        path.join(home_dir, "appdata", "local", "application data"),
        path.join(home_dir, "appdata", "local", "history"),
        path.join(home_dir, "documents"),
    ]

    def list_dir_full_path(top_lvl_):
        from string import lower
        f_list_ = []
        if top_lvl_ not in EXCLUDED_FOLDERS:
            try:
                f_list_ = listdir(top_lvl_)
                for i in range(0, len(f_list_)):
                    f_list_[i] = lower(path.join(top_lvl_, f_list_[i]))
            except WindowsError:
                # pass
                error_alert("Cannot access " + top_lvl_)

        return f_list_

    res_list = []
    target_file = lower(target_file)
    f_list = list_dir_full_path(top_lvl)

    for f in f_list:
        filename = path.split(f)[1]
        if path.isfile(filename):
            if strict:
                if target_file == filename:
                    res_list.append(f)
            else:
                if target_file in filename:
                    res_list.append(f)

        elif path.isdir(f):
            f_list.extend(list_dir_full_path(f))

    print_list(res_list)
    return res_list


def create_back_up(file_name, set_back_up_dir=""):  # backup before opening/writing to txt files
    from shutil import copy2
    from os import mkdir, path, rename, chdir, getcwd
    from datetime import datetime
    from time import time
    global backup_dir

    orig_dir = getcwd()
    # print "Creating backup copy of: ", fileName
    if path.exists(file_name) and path.isdir(file_name) is False:

        time_format = "%b-%d-%Y@%H_%M_%f"
        extension = path.splitext(file_name)[1]
        sliced_fname = path.splitext(path.split(file_name)[1])[0]  # cuts extension and path from filename

        if len(set_back_up_dir) > 0:
            backup_dir = set_back_up_dir

        dir_name = path.join(backup_dir, sliced_fname)

        if path.isdir(dir_name) is False:
            print "Creating new directory: ", dir_name
            mkdir(dir_name)

        dated_fname = "".join([sliced_fname, "@", str(datetime.now().strftime(time_format)), extension])

        try:
            copy2(file_name, dir_name)

        except IOError:
            error_alert("Error, cannot access directory or directory is invalid.", True, IOError)

        chdir(dir_name)

        if getcwd() == dir_name:
            win_error = None  # /lock?
            time_counter = 0
            init_time = time()
            while win_error is None and time_counter < MAX_WAIT_TIME:
                try:
                    dated_fname = "".join([sliced_fname, "@", str(datetime.now().strftime(time_format)), extension])
                    rename(str(path.split(file_name)[1]), dated_fname)

                    win_error = "clear"
                except:
                    time_counter = time() - init_time
                    # print "Failed to rename ", str(path.split(fileName)[1]), " to ", datedFileName

    else:
        print file_name, " is not a valid file."

    if getcwd() != orig_dir:
        chdir(orig_dir)


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
        error_alert("Passed argument: ", target, " is invalid. Must be string type argument and not an excluded process")

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


def set_console_color(color):  # include string argument? color print, change color to original
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
    msg = "ERROR: " + msg
    try:
        print msg
        set_console_color(orig_cmd_fg_color)

        if raise_exception:
            if err_class is not None:
                raise err_class(msg)
            else:
                raise Exception(msg)
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


def u_listdir(curr_dir, targ=""):
    from os import listdir, path

    f_list = listdir(unicode(curr_dir))
    for i in range(len(f_list) - 1, -1, -1):

        unicode_fname = unicode(f_list[i])
        f_list[i] = curr_dir + "\\" + unicode_fname

        if targ == "file":
            if path.isfile(f_list[i]) is False:
                f_list.remove(f_list[i])

        elif targ == "dir":
            if path.isdir(f_list[i]) is False:
                f_list.remove(f_list[i])

    if targ == "dir":
        f_list.insert(0, u"..")
        f_list.insert(0, u".")

    f_list.sort()

    return f_list


def __backup_py_n_text__():
    """
    backs up .py and txt files
    """

    from os import getcwd, listdir, getenv, path
    f_list = listdir(getenv("UtilResources"))
    path_str = getenv("UtilResources")
    for i in range(len(f_list) - 1, -1, -1):
        file_ = f_list[i]
        extension = path.splitext(file_)[1]  # extension of file
        if all([extension != ".py", extension != ".log", extension != ".txt"]):
            f_list.remove(file_)

    for file_ in f_list:
        file_ = "".join([path_str, "\\", file_])
        create_back_up(file_)


def self_validate_globals():
    root_dir_list = [music_dir, screening_dir, backup_dir, yt_amv_dir, yt_dls_dir]

    root_f_list = [song_log_file, removed_files_log, hib_log, tag_file_log, vlc_hwnd_log, deleted_tag_files_log,
                   dir_jump_file_log, tdl_log, prev_dir_log, prandom_exceptions_log, deleted_screened_log,
                   cleaned_fnames_log]

    for rd in root_dir_list:
        try:
            assert path.isdir(rd)
        except AssertionError:
            # error_alert
            raise AssertionError(rd + " is not a directory")

    for rf in root_f_list:
        try:
            assert path.isfile(rf)
        except AssertionError:
            # error_alert
            raise AssertionError(rf + " is not a file")


self_validate_globals()
