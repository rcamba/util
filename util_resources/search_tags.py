"""
*Not using .bat because it reads commas as a separator/delimiter
"""
from sys import argv, stdin, stdout
from root import switch_parser, print_list, set_clipboard_data, choose_from_list, \
    piped_list
from tag import getFilenameList, getTagList, handleTagSwitch


AVAILABLE_SWITCHES = ['s', 'f', 'r']


def main(arg_list):
    switches = switch_parser(arg_list)

    if 'f' in switches:
        _file = arg_list[0]
        tag_list = getTagList(_file)
        print tag_list

    elif 'r' in switches:
        res = handleTagSwitch("r", argList=arg_list)
        if len(res) == 1:
            f_list = map(lambda x: "\"" + x + "\"", getFilenameList(res))
            print_list(f_list)
            print res

        elif len(res) > 0:
            choose_from_tags(res)

    else:
        tags = map(lambda x_str: x_str.replace(',', ''), arg_list)

        file_list = map(lambda x: "\"" + x + "\"", getFilenameList(tags))

        if 's' in switches:
            if len(switches['s']) > 0:
                choice = file_list[int(switches['s']) - 1]

            else:
                print_list(file_list, press_to_continue=stdout.isatty())

                if len(file_list) == 1:
                    choice = file_list[0]

                else:
                    choice = choose_from_list(file_list)

            print choice
            set_clipboard_data(choice)

        else:
            if len(file_list) > 0:
                choice = file_list[len(file_list) - 1]
                set_clipboard_data(choice)
            print_list(file_list, press_to_continue=stdout.isatty())


def choose_from_tags(t_list):

    print_list(t_list)
    choice = choose_from_list(t_list)
    cf_list = getFilenameList(choice)
    print_list(cf_list)
    choice = choose_from_list(cf_list)
    set_clipboard_data(choice)


if __name__ == "__main__":

    if stdin.isatty() is False:  # for using with nf/search
        print "Piped search"
        argList = piped_list("".join(map(str, stdin.readlines())))
        main(argList)

    elif len(argv) > 1:
        main(argv[1:])

    else:

        tList = getTagList()
        tList.sort()
        choose_from_tags(tList)
