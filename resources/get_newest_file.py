"""
stores full path of newest file in the current working directory into clipboard

USAGE: nF [target string] [[-p][-#][-s]] [-f][-d]
-p: print list containing the given strings
-#: [num] number of items to print
-s: select from given list
-f: list FILES only
-d: list DIRECTORIES
"""


from sys import argv, stdin, stdout
from root import switch_parser, set_clipboard_data, \
    print_list, choose_from_list, error_alert, piped_list
from os import listdir, getcwd, stat, path
from sys import exit as sys_exit
from string import lower
AVAILABLE_SWITCHES = ['p', 's', 'd', 'h', 'f', '#']


class AttribContainer:
        pass


def sort_by_creation_time(f_list):

    for i in range(len(f_list) - 1, -1, -1):
        ac = AttribContainer()
        ac.stat = stat(f_list[i])
        ac.file = f_list[i]
        f_list[i] = ac

    f_list = sorted(f_list,
                    key=lambda AttribContainer: AttribContainer.stat.st_ctime,
                    reverse=True)

    f_list = map(lambda x: "\"" + str(x.file) + "\"", f_list)

    return f_list


def get_file_list(targ_dir=getcwd()):

    f_list = listdir(targ_dir)
    f_list = map(lower, f_list)
    return f_list


def prune_file_list(f_list, targ_words):

    for f in f_list[:]:
        removed = False

        for word in targ_words:
            if word not in f:
                f_list.remove(f)
                removed = True
                break

        if removed is False:
            if 'f' in switches:
                if path.isfile(f) is False:
                    f_list.remove(f)
                    break

            elif 'd' in switches:
                if path.isdir(f) is False:
                    f_list.remove(f)
                    break

    return f_list


def print_settings():

    # default values when empty switches
    items_to_print = 1
    aes = "none"

    if 'p' in switches:
        items_to_print = 10

        if '#' in switches:
            items_to_print = int(switches['#'])

        if len(fList) < items_to_print:
            items_to_print = len(fList)

        aes = "full"

    return items_to_print, aes


def handle_select(f_list):

    if 's' in switches:

        if len(switches['s']) > 0:
            s_val = int(switches['s'])
            if s_val <= len(f_list):
                choice = f_list[s_val - 1]
            else:
                error_alert("Select switch value:" + str(s_val) +
                           " greater than list size: " + str(len(f_list)))
                sys_exit(1)
        else:
            choice = choose_from_list(f_list)

        f_list[0] = choice

    return f_list[0]


def present_result(f_list, targ_dir=getcwd()):

    items_to_print, aes = print_settings()

    if items_to_print > 1:
        print_list(f_list, items_to_print, aes, press_to_continue=stdout.isatty())

    f_list[0] = handle_select(f_list)

    if path.isabs(f_list[0].replace("\"", '')) is False:
        f_list[0] = "\"" + targ_dir + "\\" + \
            str(f_list[0]).replace("\"", '') + "\""
        # fList[0]=path.abspath(fList[0])

    print f_list[0]

    set_clipboard_data(f_list[0])


if __name__ == "__main__":

    switches = switch_parser(argv, AVAILABLE_SWITCHES)

    if 'h' in switches:
        print __doc__

    elif stdin.isatty() is False:

        print "Piping"

        fList = piped_list("".join(map(str, stdin.readlines())))
        pruned_list = prune_file_list(fList, argv[1:])
        final_list = sort_by_creation_time(pruned_list)

    else:

        fList = get_file_list()
        pruned_list = prune_file_list(fList, argv[1:])
        final_list = sort_by_creation_time(pruned_list)

    if len(pruned_list) > 0:
        present_result(final_list)
    else:
        error_alert("Either empty directory or search term(s) not found.")
