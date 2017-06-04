import os
import sys
import copy
import collections
import simplejson as json

from root import error_alert, removed_files_log, create_backup, tag_file_log, list_from_piped, \
    key_press_input, choose_from_list, print_list, invalidated_tag_files_log, default_backup_dir


class Cache:
    tag_dict = None

    def __init__(self):
        pass


class TagException(Exception):
    pass


def validate_tag_dict_files(tag_dict):
    file_list = []
    for v in tag_dict.itervalues():
        file_list.extend(v)
    file_list = set(file_list)

    changes_made = False
    for f in file_list:
        if not os.path.isfile(f):
            removed_from_tags = []
            for tag in tag_dict.iterkeys():
                if f in tag_dict[tag]:
                    tag_dict[tag].remove(f)
                    removed_from_tags.append(tag)
                    changes_made = True
                if len(tag_dict[tag]) == 0:
                    print "Empty files list for: " + tag + "; Removing from tags"
                    del tag_dict[tag]

            m = "Removed invalid file {f_} from tags: {t_}".format(f_=f, t_=", ".join(removed_from_tags))
            print m
            log_invalid_removed_tag_and_file(m)
            error_alert("Invalid file " + f + "\n\tRemoved from: " + ", ".join(removed_from_tags))

    if changes_made:
        write_tag_file(tag_dict)

    return tag_dict


modified_time_of_reading = None


def load_tag_dict():
    global modified_time_of_reading

    if Cache.tag_dict is None or modified_time_of_reading != os.path.getmtime(tag_file_log):
        with open(tag_file_log) as reader:
            Cache.tag_dict = json.load(reader, object_pairs_hook=collections.OrderedDict)
        Cache.tag_dict = validate_tag_dict_files(Cache.tag_dict)

        modified_time_of_reading = os.path.getmtime(tag_file_log)
    return Cache.tag_dict


def log_invalid_removed_tag_and_file(log_str):
    with open(invalidated_tag_files_log, 'a') as writer:
        writer.write(log_str)
        writer.write('\n')


def log_removed_file(tag, filename):
    with open(removed_files_log, 'a') as writer:
        writer.write("{t}: {f}".format(t=tag, f=filename))
        writer.write('\n')


def log_tag_changes(type_of_change, tag, filename):
    base_tag_file_log = os.path.join(default_backup_dir, os.path.splitext(os.path.split(tag_file_log)[1])[0],
                                     "base_tag_file.log")
    tag_file_changes_log = os.path.join(default_backup_dir, os.path.splitext(os.path.split(tag_file_log)[1])[0],
                                        "tag_file_changes.log")

    if not os.path.exists(base_tag_file_log):
        print "Creating", base_tag_file_log
        with open(base_tag_file_log, 'w') as writer:
            tag_dict_str = json.dumps(load_tag_dict(), indent=2, ensure_ascii=False,
                                      encoding="utf-8", separators=(',', ': '))
            writer.write(tag_dict_str.encode("utf-8"))

    if not os.path.exists(tag_file_changes_log):
        print "Creating", tag_file_changes_log
        open(tag_file_changes_log, 'w').close()

    with open(tag_file_changes_log, 'a') as writer:
        if type_of_change == "add":
            writer.write("+ {t}:{f}".format(t=tag, f=filename))
        elif type_of_change == "remove":
            writer.write("- {t}:{f}".format(t=tag, f=filename))
        writer.write("\n")


def parse_change_line_to_tag_dict(line, tag_dict):
    type_of_change, tag_and_filename = line.split(" ", 1)
    tag, filename = tag_and_filename.split(":", 1)

    if type_of_change == "+":
        if tag in tag_dict:
            tag_dict[tag].append(filename)
            tag_dict[tag].sort()
        else:
            tag_dict[tag] = [filename]

    elif type_of_change == "-":
        tag_dict[tag].remove(filename)
        if len(tag_dict[tag]) == 0:
            del tag_dict[tag]


def merge_changes_to_base_tag_file(base_tag_file_log, tag_file_changes_log):
    print "Merging tag changes log with base file"

    with open(tag_file_changes_log) as reader:
        change_lines = reader.read().split('\n')
    with open(base_tag_file_log) as reader:
        base_tag_dict = json.load(reader, object_pairs_hook=collections.OrderedDict)

    change_lines = [l for l in change_lines if len(l) > 0]
    for line in change_lines:  # last change won't be written yet, can only validate up to all changes except last
        parse_change_line_to_tag_dict(line, base_tag_dict)

    # noinspection PyArgumentList
    base_tag_dict = collections.OrderedDict(sorted(base_tag_dict.items(), key=lambda item: item[0]))

    # validate backup similar to original log file
    orig_tag_dict = load_tag_dict()
    if base_tag_dict == orig_tag_dict:

        with open(base_tag_file_log, 'w') as writer:
            tag_dict_str = json.dumps(base_tag_dict, indent=2, ensure_ascii=False,
                                      encoding="utf-8", separators=(',', ': '))
            writer.write(tag_dict_str.encode("utf-8"))

        open(tag_file_changes_log, 'w').close()

        create_backup(base_tag_file_log, backup_dir=os.path.join(default_backup_dir, "tag_file"))

    else:
        error_alert("Backup contents not similar to original. Merge aborted!")


def write_tag_file(tag_dict):
    # noinspection PyArgumentList
    tag_dict = collections.OrderedDict(sorted(tag_dict.items(), key=lambda k: k[0]))
    for tag in tag_dict.keys():
        tag_dict[tag].sort()
    tag_dict_str = json.dumps(tag_dict, indent=2, ensure_ascii=False, encoding="utf-8", separators=(',', ': '))
    with open(tag_file_log, 'w') as writer:
        writer.write(tag_dict_str.encode("utf-8"))

    base_tag_file_log = os.path.join(default_backup_dir, os.path.splitext(os.path.split(tag_file_log)[1])[0],
                                     "base_tag_file.log")
    tag_file_changes_log = os.path.join(default_backup_dir, os.path.splitext(os.path.split(tag_file_log)[1])[0],
                                        "tag_file_changes.log")
    changes_until_merge = 10
    with open(tag_file_changes_log) as reader:
        if len(reader.readlines()) >= changes_until_merge:
            merge_changes_to_base_tag_file(base_tag_file_log, tag_file_changes_log)


def add_tags(tag_list, filename, verbose=False):
    if not os.path.isabs(filename):
        error_alert("{f} must be in absolute full file path".format(f=filename),
                    raise_exception=True, err_class=TagException)

    if not os.path.isfile(filename):
        error_alert(filename + " is not a valid file", raise_exception=True, err_class=IOError)

    tag_dict = load_tag_dict()
    filename = os.path.normpath(filename.lower())
    appended_list = []
    for tag in tag_list:
        tag = tag.strip().lower()
        if tag not in tag_dict:
            print "Creating new tag:", tag
            tag_dict[tag] = [filename]
            log_tag_changes("add", tag, filename)
        elif filename not in tag_dict[tag]:
            tag_dict[tag].append(filename)
            appended_list.append(tag)
            log_tag_changes("add", tag, filename)
        else:
            error_alert(filename + " is already in tag: " + tag)

    if verbose and len(appended_list) > 0:
        print "Appended to tags:", ", ".join(appended_list)
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


def remove_file_from_tags(tag_list, fname, verbose=True):
    tag_dict = load_tag_dict()
    fname = os.path.normpath(fname.lower())
    for tag in tag_list:
        tag = tag.strip().lower()
        if fname in tag_dict[tag]:
            log_tag_changes("remove", tag, fname)
            if verbose:
                print "Removed {f} from {t}".format(f=fname.encode("unicode_escape"), t=tag)

            tag_dict[tag].remove(fname)
            if len(tag_dict[tag]) == 0:
                print "Empty files list for: " + tag + "; Removing from tags."
                del tag_dict[tag]
        else:
            error_alert("Tag: " + tag + " doesn't have filename: " + fname)
    log_removed_file(fname, ", ".join(tag_list))
    write_tag_file(tag_dict)


def get_files_from_tags(tag_list):  # str or list
    if type(tag_list) == str:
        tag_list = [tag_list]

    tag_dict = load_tag_dict()
    file_list = []

    for tag in tag_list:
        tag = tag.strip().lower()
        if tag in tag_dict:
            if len(file_list) == 0:
                file_list = copy.deepcopy(tag_dict[tag])
            else:
                file_list = list(set(file_list).intersection(
                    copy.deepcopy(tag_dict[tag])))
        else:
            error_alert("Tag: {t} not found ".format(t=tag), raise_exception=True, err_class=TagException)

    file_list.sort()
    return file_list


def get_tags_for_file(filename=None):
    tag_dict = load_tag_dict()

    if filename is None:
        tags = tag_dict.keys()
    else:
        tags = []
        filename = os.path.normpath(filename.lower())
        if not os.path.isfile(filename):
            error_alert(filename + " is not a valid file", raise_exception=True, err_class=IOError)

        for tag in tag_dict.keys():
            if filename in tag_dict[tag]:
                tags.append(tag)

    return tags  # sorted by default since using OrderedDict


def get_mixed_files_from_tags(tag_list):  # for prand + search
    tag_dict = load_tag_dict()
    mixed_files = []
    for tag in tag_list:
        tag = tag.strip().lower()
        if tag in tag_dict:
            mixed_files.extend(copy.deepcopy(tag_dict[tag]))
        else:
            error_alert("Tag doesn't exist: " + tag, raise_exception=True, err_class=TagException)

    mixed_files = set(mixed_files)
    return mixed_files


def get_tag_by_partial_match(partial_tag_match):
    tag_dict = load_tag_dict()
    possible_matches = []
    for tag in tag_dict.keys():
        tag = tag.strip().lower()
        if partial_tag_match.lower() in tag:
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
        input_tag_list = map(str.strip, input_tag_list)
        if not os.path.isabs(sys.argv[1]):
            add_tags(input_tag_list, os.path.join(os.getcwd(), sys.argv[1]), verbose=True)
        else:
            add_tags(input_tag_list, sys.argv[1], verbose=True)

    elif sys.stdin.isatty() is False:
        print "Tagging piped items"
        fileList = list_from_piped("".join(map(str, sys.stdin.readlines())))
        input_tag_list = key_press_input("Enter tag(s). Separate with commas").split(',')
        for t in input_tag_list:
            tag_multiple_files(t, fileList)
    else:
        print "Missing full path file argument"
