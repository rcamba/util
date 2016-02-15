# tag_rename

from sys import argv
from tag import getTagList
from os import rename, path, getcwd
from tag import addTags, removeTags


def tag_rename(orig_name, new_name):

    if path.isfile(orig_name):
        if path.isabs(orig_name) is False:
            orig_name = path.join(getcwd(), orig_name)

        tag_list = getTagList(orig_name)
        if len(tag_list) == 0:
            raise ValueError("No tags found for {}".format(orig_name))

        if path.isabs(new_name) is False:
            new_name = path.join(path.split(orig_name)[0], new_name)

        print "Removing {tl} from {f}\n".format(tl=tag_list, f=orig_name)
        removeTags(tag_list, orig_name)

        print "Renaming {src} to {dest}\n".format(src=orig_name, dest=new_name)
        rename(orig_name, new_name)

        tag_str = ", ".join(map(str, tag_list))
        print "Tagging {dest} with {tags}\n".format(
            dest=new_name, tags=tag_str)
        addTags(tag_list, new_name)

    else:
        print "Error: Invalid file for first argument"


if __name__ == "__main__":

    if len(argv) == 3:
        orig_name = argv[1]
        new_name = argv[2]
        tag_rename(orig_name, new_name)

    else:
        print "Missing arguments."
        print "Usage tag_rename.py [source_file] [destination_file]"
