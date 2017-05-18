from argparse import ArgumentParser
from os import listdir, chdir, getcwd, path, rename
from sys import exit as sys_exit
from string import ascii_letters, digits, punctuation

from root import screening_dir, error_alert, cleaned_fnames_log
from tag import tagMultipleFiles, getFilenameList
from kanji_to_romaji import kanji_to_romaji


def write_line_to_log(line):
    with open(cleaned_fnames_log, 'a') as writer:
        writer.write(line)
        writer.write("\n")


def screen_tagging():
    """Tags all files in screening_dir with 'screen' tag"""

    chdir(screening_dir)
    if getcwd() == screening_dir:
        print "Starting screen tagging"

        file_list = listdir(screening_dir)
        screening_list = getFilenameList("screen")
        removed_counter = 0
        for i in range(len(file_list) - 1, -1, -1):
            file_list[i] = path.join(screening_dir, file_list[i]).lower()

            if file_list[i] in screening_list:
                file_list.remove(file_list[i])
                removed_counter += 1

        tagMultipleFiles("screen", file_list)
        print removed_counter, " songs already had screen tag"
        print "Tagged ", len(file_list), " files"

    else:
        print "Wrong directory: Need screening directory"


def clean_file_names(directory):

    file_list = listdir(unicode(directory))

    changes_dict = {}

    for f in file_list:

        cleaned = clean_string(f)

        if f != cleaned:
            changes_dict[f] = cleaned

    return changes_dict


def clean_chars(partial_clean_str):

    valid_chars = list(ascii_letters) + list(digits) + [" "] + \
                  list(punctuation
                       .replace('\\', '')
                       .replace('/', '')
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

    while "  " in cleaned:
        cleaned = cleaned.replace("  ", " ")

    return cleaned


def clean_string(dirty_str):
    kanji_cleaned_str = kanji_to_romaji(dirty_str)
    if "\u" in kanji_cleaned_str:
        untranslated_warn_msg = "Untranslated unicode character found in " + kanji_cleaned_str
        error_alert(untranslated_warn_msg)
        if not args.dry_run:
            write_line_to_log(untranslated_warn_msg)

    cleaned = clean_chars(kanji_cleaned_str)

    token = path.splitext(cleaned)
    fn_only = token[0]
    result = cleaned

    if len(cleaned) == 0 or len(fn_only) == 0:
        all_inval_warn_msg = dirty_str.encode("unicode_escape") + \
                             " only consists of invalid characters. Cannot be cleaned."
        error_alert(all_inval_warn_msg)
        if not args.dry_run:
            write_line_to_log(all_inval_warn_msg)
        result = dirty_str

    return result


def rename_files(changes_dict, directory):
    with open(cleaned_fnames_log, 'a') as writer:
        for key in changes_dict.keys():
            try:
                rename(path.join(directory, key),
                       path.join(directory, changes_dict[key]))
                writer.write(key.encode('utf8') + ": " + changes_dict[key])
                writer.write("\n")

            except WindowsError, e:
                error_alert("Unable to rename " + key.encode("unicode_escape") + " in to " +
                            changes_dict[key].encode("unicode_escape") + ". Stopping program." +
                            "\n" + str(e))
                sys_exit(1)


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
