from argparse import ArgumentParser
from sys import stdin, stdout
from os import listdir, getcwd, stat, path
from root import set_clipboard_data, \
    print_list, choose_from_list, error_alert, list_from_piped


class AttribContainer:
    def __init__(self):
        pass


def sort_by_creation_time(f_list_):
    for i in range(len(f_list_) - 1, -1, -1):
        ac = AttribContainer()
        ac.stat = stat(f_list_[i])
        ac.file = f_list_[i]
        f_list_[i] = ac

    f_list_ = sorted(f_list_,
                     key=lambda ac_: ac_.stat.st_ctime,
                     reverse=True)

    return f_list_


def get_file_list(targ_dir=getcwd()):
    f_list_ = [path.join(targ_dir, f) for f in listdir(unicode(targ_dir))]

    if args.files_only:
        f_list_ = [f for f in f_list_ if path.isfile(f)]

    elif args.dir_only:
        f_list_ = [f for f in f_list_ if path.isdir(f)]

    return f_list_


def prune_targ_words_from_file_list(f_list_, targ_words):
    for word in targ_words:
        for f in f_list_[:]:
            if word.lower() not in path.split(f)[1].lower():
                f_list_.remove(f)
    return f_list_


def select_item_from_files(f_list_, numbered_index):
    chosen_item = f_list_[numbered_index - 1]
    if numbered_index == -1:  # prompt to select
        chosen_item = choose_from_list(f_list_)

    return chosen_item


def present_result(f_list_, display_full_filepath):
    if args.list_files is not None or args.select_file is not None:
        if args.list_files == -1:
            if len(args.targ_words) > 0:
                args.list_files = len(f_list_)
            else:
                args.list_files = 10

        if display_full_filepath:
            list_to_be_printed = f_list_
        else:
            list_to_be_printed = [path.split(f)[1] for f in f_list_]
        print_list(list_to_be_printed, args.list_files, press_to_continue=stdout.isatty())

    quoted_f_list = map(lambda x: "\"" + str(x) + "\"", f_list_)
    chosen_item = quoted_f_list[0]

    if args.select_file is not None:
        chosen_item = select_item_from_files(quoted_f_list, args.select_file)

    print chosen_item
    set_clipboard_data(chosen_item)


def add_arg_options():
    p = ArgumentParser()
    p.add_argument('targ_words', nargs='*')
    p.add_argument("-l", "--list-files", help="list the x newest files. default x is 10",
                   type=int, nargs="?", const=-1, required=False)
    p.add_argument("-f", "--files-only", help="only show files",
                   action="store_true")
    p.add_argument("-d", "--dir-only", help="only show directories",
                   action="store_true")
    p.add_argument("-s", "--select-file", help="select file among list",
                   type=int, nargs="?", const=-1, required=False)

    return p


def get_newest_file(args_):
    global args
    args = args_

    if stdin.isatty() is False:
        print "Piping"
        f_list = list_from_piped("".join(map(str, stdin.readlines())))
        display_full_filepath = True

    else:
        f_list = get_file_list()
        display_full_filepath = False

    pruned_list = prune_targ_words_from_file_list(f_list, args_.targ_words)
    sorted_list_ac = sort_by_creation_time(pruned_list)
    sorted_list = map(lambda x: str(x.file.encode("unicode_escape")), sorted_list_ac)
    if len(sorted_list) > 0:
        present_result(sorted_list, display_full_filepath)
    else:
        error_alert("Either empty directory or search term(s) not found.")


if __name__ == "__main__":
    parser = add_arg_options()
    args = parser.parse_args()
    get_newest_file(args)
