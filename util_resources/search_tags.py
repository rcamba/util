"""
Not using .bat because it reads commas as a separator/delimiter
"""
from os import path, getcwd
from argparse import ArgumentParser
from sys import stdin, stdout
from root import print_list, set_clipboard_data, choose_from_list, piped_list, error_alert
from tag import get_files_from_tags, get_tags_for_file, get_tag_by_partial_match, get_mixed_files_from_tags


def set_args(new_args):
    global args
    args = new_args


def present_result(file_list):
    file_list = map(lambda f_: "\"" + f_ + "\"", file_list)
    if args.num_of_results is not None:
        file_list = file_list[:args.num_of_results]

    print_list(file_list, press_to_continue=stdout.isatty())

    if args.select:
        if len(file_list) == 1:
            choice = file_list[0]

        else:
            choice = choose_from_list(file_list)
            print choice

        set_clipboard_data(choice)


def prune_exceptions_from_file_list(file_list, exception_list):
    if exception_list is not None and len(exception_list) > 0:
        exception_file_list = get_files_from_tags(exception_list)
        for f in file_list:
            if f not in exception_file_list:
                file_list.remove(f)


def search(tag_list, exception_list=None):
    if len(args.search_filename) > 0:
        if not path.isabs(args.search_filename):
            args.search_filename = path.join(getcwd(), args.search_filename)
        args.search_filename = path.realpath(args.search_filename)
        if not path.isfile(args.search_filename):
            raise IOError("{f} is not a valid file".format(f=args.search_filename))

        tag_list = get_tags_for_file(args.search_filename)
        print tag_list

    elif args.partial_match:
        tag = get_tag_by_partial_match(tag_list[0])

        if tag is None:
            raise Exception("No tag found matching: " + tag_list[0])

        file_list = get_files_from_tags(tag)

        prune_exceptions_from_file_list(file_list, exception_list)
        print tag
        present_result(file_list)

    else:
        if args.mix_tags:
            file_list = get_mixed_files_from_tags(tag_list)
        else:
            file_list = get_files_from_tags(tag_list)

        if len(file_list) == 0:
            raise Exception("No files found for given tag(s): " + ", ".join(tag_list))

        prune_exceptions_from_file_list(file_list, exception_list)
        present_result(file_list)


def choose_from_tags(t_list_):
    print_list(t_list_)
    choice = choose_from_list(t_list_)
    cf_list = get_files_from_tags(choice)
    present_result(cf_list)


def create_args():
    p = ArgumentParser()
    group = p.add_mutually_exclusive_group()

    p.add_argument("tags", type=str, nargs='*', help="tags split by comma")

    p.add_argument("-n", "--num", type=int, help="number of songs to play", dest="num_of_results")
    p.add_argument("-m", "--mix", action="store_true", help="mix tags", dest="mix_tags")
    p.add_argument("-e", "--except", nargs='+', default=[], help="mix tags", dest="exception_tags")

    p.add_argument("-s", "--select", action="store_true", dest="select")

    group.add_argument("-f", "--file-search", type=str, default="", dest="search_filename")
    group.add_argument("-r", "--partial", action="store_true", dest="partial_match")

    return p


def parse_args(p):
    args_ = p.parse_args()
    args_.tags = [t.strip() for t in " ".join(args_.tags).split(",") if len(t) > 0]
    args_.exception_tags = [et for et in " ".join(args_.exception_tags).split(",") if len(et) > 0]
    return args_


def do_search(args_):
    global args
    args = args_
    if stdin.isatty() is False:  # for using with nf/search
        print "Piped search"
        arg_list = piped_list("".join(map(str, stdin.readlines())))
        search(arg_list)

    elif len(args.tags) > 0:
        search(args.tags, args.exception_tags)

    else:
        t_list = get_tags_for_file()
        t_list.sort()
        choose_from_tags(t_list)


if __name__ == "__main__":
    parser = create_args()
    args = parse_args(parser)
    do_search(args)

