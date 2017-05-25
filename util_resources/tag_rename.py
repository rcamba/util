from sys import argv
from tag import get_tags_for_file
from os import rename, path, getcwd
from tag import add_tags, remove_file_from_tags, TagException


def tag_rename(orig_name, new_name, verbose=False, allow_empty_tags=True):
    if not path.isabs(orig_name):
        orig_name = path.realpath(path.join(getcwd(), orig_name))

    if path.isdir(new_name):
        new_name = path.realpath(path.join(new_name, path.split(orig_name)[1]))
    elif not path.isabs(new_name):
        new_name = path.realpath(path.join(getcwd(), new_name))

    if not path.isfile(orig_name):
        raise IOError("Error: Invalid file {f}.".format(f=orig_name))
    if orig_name == new_name:
        raise ValueError("The source and destination are the same.")

    orig_name = orig_name.lower()
    new_name = new_name.lower()

    tag_list = get_tags_for_file(orig_name)
    if not allow_empty_tags and len(tag_list) == 0:  # for cleanfnames
        raise ValueError("No tags found for {}".format(orig_name))

    if verbose:
        print "Removing {tl} from {f}\n".format(tl=tag_list, f=orig_name)
    remove_file_from_tags(tag_list, orig_name, False)

    try:
        if verbose:
            print "Renaming {src} to {dest}\n".format(src=orig_name, dest=new_name)
        rename(orig_name, new_name)

    except WindowsError:
        add_tags(tag_list, orig_name)
        raise

    try:
        tag_str = ", ".join(map(str, tag_list))
        if verbose:
            print "Tagging {dest} with {tags}\n".format(dest=new_name, tags=tag_str)
        add_tags(tag_list, new_name)

    except TagException:
        rename(new_name, orig_name)
        add_tags(tag_list, orig_name)
        raise

if __name__ == "__main__":

    if len(argv) == 3:
        tag_rename(orig_name=argv[1], new_name=argv[2], verbose=True, allow_empty_tags=False)

    else:
        print "Missing arguments."
        print "Usage tag_rename.py [source_file] [destination_file]"
