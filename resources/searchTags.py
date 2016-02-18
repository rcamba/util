"""
*Not using .bat because it reads commas as a separator/delimiter
"""
from sys import argv, stdin, stdout
from root import switchParser, printList, setClipboardData, chooseFromList, \
    pipedList
from tag import getFilenameList, getTagList, handleTagSwitch


AVAILABLE_SWITCHES = ['s', 'f', 'r']


def main(arg_list):
    switches = switchParser(arg_list)

    if 'f' in switches:
        _file = arg_list[0]
        tag_list = getTagList(_file)
        print tag_list

    elif 'r' in switches:
        res = handleTagSwitch("r", argList=arg_list)
        if len(res) == 1:
            f_list = map(lambda x: "\"" + x + "\"", getFilenameList(res))
            printList(f_list)
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
                printList(file_list, pressToContinue=stdout.isatty())

                if len(file_list) == 1:
                    choice = file_list[0]

                else:
                    choice = chooseFromList(file_list)

            print choice
            setClipboardData(choice)

        else:
            if len(file_list) > 0:
                choice = file_list[len(file_list) - 1]
                setClipboardData(choice)
            printList(file_list, pressToContinue=stdout.isatty())


def choose_from_tags(t_list):

    printList(t_list)
    choice = chooseFromList(t_list)
    cf_list = getFilenameList(choice)
    printList(cf_list)
    choice = chooseFromList(cf_list)
    setClipboardData(choice)


if __name__ == "__main__":

    if stdin.isatty() is False:  # for using with nf/search
        print "Piped search"
        argList = pipedList("".join(map(str, stdin.readlines())))
        main(argList)

    elif len(argv) > 1:
        main(argv[1:])

    else:

        tList = getTagList()
        tList.sort()
        choose_from_tags(tList)
