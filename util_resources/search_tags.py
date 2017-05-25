from sys import argv
from json import load
from os import path, getcwd
from argparse import ArgumentParser, FileType
from sys import stdin, stdout
from root import print_list, set_clipboard_data, choose_from_list, song_log_file
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


def search_tags(tag_list, exception_list=None):
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

    p.add_argument('infile', nargs='?', type=FileType('r'), default=stdin)
    p.add_argument('outfile', nargs='?', type=FileType('w'), default=stdout)

    group.add_argument("-f", "--file-search", type=str, default="", nargs="?", dest="search_filename")
    group.add_argument("-pc", "--play-count", type=str, default="", dest="play_count_filename")
    group.add_argument("-r", "--partial", action="store_true", dest="partial_match")

    return p


def parse_args(p):
    args_ = p.parse_args()
    args_.tags = [t.strip() for t in " ".join(args_.tags).split(",") if len(t) > 0]
    args_.exception_tags = [et for et in " ".join(args_.exception_tags).split(",") if len(et) > 0]
    return args_


def search_partial_match(partial_tag_str, exception_tags_list):
    tag = get_tag_by_partial_match(partial_tag_str)

    if tag is None:
        raise Exception("No tag found matching: " + partial_tag_str)

    file_list = get_files_from_tags(tag)

    prune_exceptions_from_file_list(file_list, exception_tags_list)
    print tag
    present_result(file_list)


def search_tags_for_file(filename):
    if not path.isabs(filename):
        filename = path.join(getcwd(), filename)
    filename = path.realpath(filename)
    if not path.isfile(filename):
        raise IOError("{f} is not a valid file".format(f=filename))

    tag_list = get_tags_for_file(filename)
    print filename
    if len(tag_list) == 0:
        print "No tags"
    else:
        print ", ".join(tag_list)


def search_for_song_playcount(song_filename):
    with open(song_log_file) as reader:
        song_log_dict = load(reader)
    song_filename = song_filename.replace("\"", "").strip()
    if song_filename in song_log_dict:
        print song_filename
        print song_log_dict[song_filename]["play_count"], "play(s)"
    else:
        print song_filename, "not found in songs log."


def do_search(parser):
    global args

    if stdin.isatty() is False:  # for using with nf/search
        print "Piped search"

        piped_fname = stdin.readlines()[2].strip().replace("\"", "")
        argv.append(piped_fname)
        loc_args = parser.parse_args(argv)
    else:
        loc_args = parse_args(parser)

    args = loc_args
    if len(loc_args.play_count_filename) > 0:
        search_for_song_playcount(loc_args.play_count_filename)

    elif len(loc_args.search_filename) > 0:
        search_tags_for_file(loc_args.search_filename)

    elif loc_args.partial_match:
        search_partial_match(loc_args.tags[0], loc_args.exception_tags)

    elif len(loc_args.tags) > 0:
        search_tags(loc_args.tags, loc_args.exception_tags)

    else:
        t_list = get_tags_for_file()
        t_list.sort()
        choose_from_tags(t_list)


if __name__ == "__main__":
    parser_ = create_args()
    do_search(parser_)

