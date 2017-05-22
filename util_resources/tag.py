import os
import sys
import collections
import simplejson as json

from root import error_alert, removed_files_log, create_back_up, tag_file_log, piped_list, \
    key_press_input, choose_from_list, print_list


class Cache:  # caching
    tag_dict = None

    def __init__(self):
        pass


def validate_tag_dict_files(tag_dict):
    file_list = []
    [file_list.extend(v) for v in tag_dict.values()]
    file_list = set(file_list)

    changes_made = False
    for f in file_list:
        if not os.path.isfile(f):
            removed_from_tags = []
            for tag in tag_dict.keys():
                if f in tag_dict[tag]:
                    tag_dict[tag].remove(f)
                    removed_from_tags.append(tag)
                    changes_made = True
                if len(tag_dict[tag]) == 0:
                    print "Empty files list for: " + tag + "; Removing from tags"
                    del tag_dict[tag]

            log_removed_file("Removed invalid file " + f + "from tags:" + ", ".join(removed_from_tags))
            error_alert("Invalid file " + f + "\n\tRemoved from: " + ", ".join(removed_from_tags))

    if changes_made:
        write_tag_file(tag_dict)

    return tag_dict


def load_tag_dict():
    if Cache.tag_dict is None:
        with open(tag_file_log) as reader:
            tag_dict = json.load(reader, object_pairs_hook=collections.OrderedDict)

        Cache.tag_dict = validate_tag_dict_files(tag_dict)

    return Cache.tag_dict


def log_removed_file(log_str):
    with open(removed_files_log, 'a') as writer:
        writer.write(log_str)
        writer.write('\n')


def write_tag_file(tag_dict):
    # noinspection PyArgumentList
    tag_dict = collections.OrderedDict(sorted(tag_dict.items(), key=lambda k: k[0]))
    for tag in tag_dict.keys():
        tag_dict[tag].sort()
    create_back_up(tag_file_log)
    with open(tag_file_log, 'w') as writer:
        json.dump(tag_dict, writer, indent=2, separators=(',', ': '))


def add_tags(tag_list, filename):
    if not os.path.isabs(filename):
        error_alert("filename argument must be absolute full file path", raise_exception=True)

    if not os.path.isfile(filename):
        error_alert(filename + " is not a valid file", raise_exception=True, err_class=IOError)

    tag_dict = load_tag_dict()
    for tag in tag_list:
        if tag not in tag_dict:
            tag_dict[tag] = [filename]
        elif filename not in tag_dict[tag]:
            tag_dict[tag].append(filename)
        else:
            error_alert(filename + " is already in tag: " + tag)

    write_tag_file(tag_dict)


def remove_invalid_files(file_list):
    for f in file_list[:]:
        if not os.path.isfile(f):
            error_alert(f + " is not a valid file. Removing from file list.")
            file_list.remove(f)


def tag_multiple_files(tag, file_list):
    remove_invalid_files(file_list)

    if len(file_list) > 0:
        for f in file_list:
            add_tags([tag], f)

    else:
        error_alert("No valid file to add. No changes have been made.")


def remove_file_from_tags(tag_list, filename):
    tag_dict = load_tag_dict()
    for tag in tag_list:
        if filename in tag_dict[tag]:
            tag_dict[tag].remove(filename)
            if len(tag_dict[tag]) == 0:
                print "Empty files list for: " + tag + "; Removing from tags."
                del tag_dict[tag]
        else:
            error_alert("Tag:" + tag + " doesn't have filename : " + filename)

    write_tag_file(tag_dict)


def get_files_from_tags(tag_list):  # str or list
    if type(tag_list) == str:
        tag_list = [tag_list]

    tag_dict = load_tag_dict()
    file_list = []

    for tag in tag_list:
        if tag in tag_dict:
            if len(file_list) == 0:
                file_list = tag_dict[tag]
            else:
                file_list = list(set(file_list).intersection(tag_dict[tag]))
        else:
            error_alert("Tag: {t} not found ".format(t=tag), raise_exception=True)

    file_list.sort()
    return file_list


def get_tags_for_file(filename=None):
    tag_dict = load_tag_dict()

    if filename is None:
        tags = tag_dict.keys()
    else:
        tags = []
        if not os.path.isfile(filename):
            error_alert(filename + " is not a valid file", raise_exception=True, err_class=IOError)

        for tag in tag_dict.keys():
            if filename in tag_dict[tag]:
                tags.append(tag)
    return tags # sorted by default since using OrderedDict


def get_mixed_files_from_tags(tag_list):  # for prand + search
    tag_dict = load_tag_dict()
    mixed_files = []
    for tag in tag_list:
        if tag in tag_dict:
            mixed_files.extend(tag_dict[tag])
        else:
            error_alert("Tag doesn't exist: " + tag, raise_exception=True)

    mixed_files = set(mixed_files)
    return mixed_files


def get_tag_by_partial_match(partial_tag_match):
    tag_dict = load_tag_dict()
    possible_matches = []
    for tag in tag_dict.keys():
        if partial_tag_match in tag:
            possible_matches.append(tag)

    choice = None

    if len(possible_matches) > 1:
        print_list(possible_matches)
        choice = choose_from_list(possible_matches)
    elif len(possible_matches) > 0:
        choice = possible_matches[0]
    return choice


if __name__ == "__main__":

    if len(sys.argv) > 1:
        input_tag_list = raw_input("Enter tag(s). Separate with commas\n").split(',')
        if not os.path.isabs(sys.argv[1]):
            add_tags(input_tag_list, os.path.join(os.getcwd(), sys.argv[1]))
        else:
            add_tags(input_tag_list, sys.argv[1])

    elif sys.stdin.isatty() is False:
        print "Tagging piped items"
        fileList = piped_list("".join(map(str, sys.stdin.readlines())))
        input_tag_list = key_press_input("Enter tag(s). Separate with commas").split(',')
        for t in input_tag_list:
            tag_multiple_files(t, fileList)
    else:
        print "Missing full path file argument"
