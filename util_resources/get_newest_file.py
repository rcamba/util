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
            if word.lower() not in f.lower():
                f_list_.remove(f)
    return f_list_


def select_item_from_files(f_list_, numbered_index):
    chosen_item = f_list_[numbered_index - 1]
    if numbered_index == -1:  # prompt to select
        chosen_item = choose_from_list(f_list_)

    return chosen_item


def present_result(f_list_):
    if args.list_files is not None or args.select_file is not None:
        if args.list_files is None:
            args.list_files = 10
        print_list([path.split(f)[1] for f in f_list_], args.list_files, press_to_continue=stdout.isatty())

    chosen_item = f_list_[0]

    if args.select_file is not None:
        chosen_item = select_item_from_files(f_list_, args.select_file)

    print chosen_item
    set_clipboard_data(chosen_item)


def add_arg_options():
    p = ArgumentParser()
    p.add_argument('targ_words', nargs='*')
    p.add_argument("-l", "--list-files", help="list the x newest files. default x is 10",
                   type=int, nargs="?", const=10, required=False)
    p.add_argument("-f", "--files-only", help="only show files",
                   action="store_true")
    p.add_argument("-d", "--dir-only", help="only show directories",
                   action="store_true")
    p.add_argument("-s", "--select-file", help="select file among list",
                   type=int, nargs="?", const=-1, required=False)

    return p


if __name__ == "__main__":
    parser = add_arg_options()
    args = parser.parse_args()

    if stdin.isatty() is False:
        print "Piping"
        f_list = list_from_piped("".join(map(str, stdin.readlines())))

    else:
        f_list = get_file_list()

    pruned_list = prune_targ_words_from_file_list(f_list, args.targ_words)
    sorted_list = sort_by_creation_time(pruned_list)
    final_quoted_list = map(lambda x: "\"" + str(x.file.encode("unicode_escape")) + "\"", sorted_list)

    if len(final_quoted_list) > 0:
        present_result(final_quoted_list)
    else:
        error_alert("Either empty directory or search term(s) not found.")
