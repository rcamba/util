from argparse import ArgumentParser
from os import listdir, chdir, getcwd, path, rename
from sys import exit as sys_exit
from string import ascii_letters, digits, punctuation

from root import screening_dir, error_alert, cleaned_fnames_log, stdout_write
from tag import tag_multiple_files, get_files_from_tags
from tag_rename import tag_rename
from kanji_to_romaji import kanji_to_romaji


def _undo_rename(cleaned_targ_fname):
    if not path.isabs(cleaned_targ_fname):
        raise IOError("Filename must be in full/absolute path.")

    cleaned_targ_fname = path.realpath(cleaned_targ_fname)
    targ_dir = path.dirname(cleaned_targ_fname)
    cleaned_targ_fname = path.split(cleaned_targ_fname)[1]

    with open(cleaned_fnames_log) as reader:
        lines = reader.read().split('\n')
        for line in lines:
            if len(line) > 0:
                orig_fname, cleaned_fname = line.split(': ')
                if cleaned_targ_fname.lower() == cleaned_fname.lower():
                    tag_rename(path.join(targ_dir, cleaned_targ_fname),
                               path.join(targ_dir, orig_fname),
                               verbose=True, allow_empty_tags=True)


def append_line_to_log(line):
    with open(cleaned_fnames_log, 'a') as writer:
        writer.write(line)
        writer.write("\n")


def screen_tagging():
    """Tags all files in screening_dir with 'screen' tag"""

    chdir(screening_dir)
    if getcwd() == screening_dir:
        print "Starting screen tagging"

        file_list = listdir(screening_dir)
        screening_list = get_files_from_tags("screen")
        removed_counter = 0
        for i in range(len(file_list) - 1, -1, -1):
            file_list[i] = path.join(screening_dir, file_list[i])

            if file_list[i] in screening_list:
                file_list.remove(file_list[i])
                removed_counter += 1

        tag_multiple_files("screen", file_list)
        print removed_counter, " songs already had screen tag"
        print "Tagged ", len(file_list), " files"

    else:
        print "Wrong directory: Need screening directory"


def clean_file_names(directory):

    file_list = listdir(unicode(directory))

    changes_dict = {}

    for file_ in file_list:
        fname, ext = path.splitext(file_)
        cleaned_fname = clean_string(fname, not args.dry_run)
        cleaned_file = cleaned_fname + ext
        if file_ != cleaned_file:
            changes_dict[file_] = cleaned_file

    return changes_dict


def clean_chars(partial_clean_str):

    valid_chars = list(ascii_letters) + list(digits) + [" "] + \
                  list(punctuation
                       .replace('\\', '')
                       .replace('/', '')
                       .replace(':', '')
                       .replace('*', '')
                       .replace('?', '')
                       .replace('\"', '')
                       .replace('<', '')
                       .replace('>', '')
                       .replace('|', ''))

    cleaned = ""

    # clean invalid chars
    for c in partial_clean_str:
        if c in valid_chars:
            cleaned = "".join([cleaned, c])

    # clean extra spaces
    tokens = path.splitext(cleaned)
    cleaned = tokens[0]
    cleaned = cleaned.strip()
    cleaned += tokens[1]

    cleaned = cleaned.replace("( ", "(")
    cleaned = cleaned.replace(" )", ")")
    cleaned = cleaned.replace("[ ", "[")
    cleaned = cleaned.replace(" ]", "]")
    cleaned = cleaned.replace("]", "] ")

    cleaned = cleaned.strip()
    while "  " in cleaned:
        cleaned = cleaned.replace("  ", " ")

    return cleaned


def clean_string(dirty_str, log_warnings=False):
    kanji_cleaned_str = kanji_to_romaji(dirty_str)
    if "\u" in kanji_cleaned_str:
        untranslated_warn_msg = "Untranslated unicode character found in " + kanji_cleaned_str
        error_alert(untranslated_warn_msg)
        if log_warnings:
            append_line_to_log(untranslated_warn_msg)

    cleaned = clean_chars(kanji_cleaned_str)

    token = path.splitext(cleaned)
    fn_only = token[0]
    result = cleaned

    if len(cleaned) == 0 or len(fn_only) == 0:
        all_inval_warn_msg = dirty_str.encode("unicode_escape") + \
                             " only consists of invalid characters. Cannot be cleaned."
        error_alert(all_inval_warn_msg)
        if log_warnings:
            append_line_to_log(all_inval_warn_msg)
        result = dirty_str

    return result


def rename_files(changes_dict, directory):
    with open(cleaned_fnames_log, 'a') as writer:  # log renaming changes
        for key in changes_dict.keys():
            stdout_write("Renamed {n} out of {t} files".format(n=changes_dict.keys().index(key) + 1,
                                                               t=len(changes_dict.keys())))
            try:
                orig_name = path.join(directory, key)
                new_name = path.join(directory, changes_dict[key])
                if path.isfile(orig_name):  # dir won't have tags
                    tag_rename(orig_name, new_name)
                else:
                    rename(orig_name, new_name)
                writer.write(key.encode('utf-8') + ": " + changes_dict[key])
                writer.write("\n")

            except WindowsError, e:
                error_alert("Unable to rename " + key.encode("unicode_escape") + " in to " +
                            changes_dict[key].encode("unicode_escape") + ". Stopping program." +
                            "\n" + str(e))
                sys_exit(1)
    print ""  # newline for messages after stdout_write


def main(directory):
    if path.isdir(directory):
        changes_dict = clean_file_names(directory)

        if args.verbose:
            for key in changes_dict.keys():
                print key.encode("unicode_escape") + " ---> " + changes_dict[key]

        if args.dry_run:
            print "Dry-run: printing only. No file changes have been made."
            print str(len(changes_dict)) + " files would have been renamed."

        else:
            rename_files(changes_dict, directory)
            print "renamed " + str(len(changes_dict)) + " files."

            if path.realpath(directory) == path.realpath(screening_dir):
                screen_tagging()

    else:
        error_alert("Argument must be a valid directory")
        sys_exit(1)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("targ_dir", help="require directory argument to be explicit; accepts '%CD%' or '.'")  #
    parser.add_argument("-d", "--dry-run", help="run and show filename changes without renaming files",
                        action="store_true")
    parser.add_argument("-v", "--verbose", help="print filename and renamed filename",
                        action="store_true")

    args = parser.parse_args()

    main(unicode(args.targ_dir))
