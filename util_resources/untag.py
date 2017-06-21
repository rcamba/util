import argparse
from tag import remove_file_from_tags, get_tags_for_file, get_files_from_tags, TagException
from root import print_list, keypress_input, error_alert


def get_user_choices(tag_or_file_list):

    choice_list = []
    print_list(tag_or_file_list)
    if len(tag_or_file_list) > 1:
        print "Enter number(s) separated by commas"

        try:
            input_ = raw_input()
        except EOFError:  # pipes
            input_ = keypress_input()

        choices = input_.split(',')
        choices = map(int, choices)

        for choice in choices:
            choice_list.append(tag_or_file_list[choice - 1])

    else:
        choice_list.append(tag_or_file_list[0])

    return choice_list


def remove_files_from_tag(tag):

    try:
        f_list = get_files_from_tags(tag)
        choice_list = get_user_choices(f_list)
        for chosen_file in choice_list:
            remove_file_from_tags([tag], chosen_file)
    except TagException as e:
        error_alert(str(e))


def remove_tags_from_filename(filename):

    tag_list = get_tags_for_file(filename)
    if len(tag_list) > 0:
        choice_list = get_user_choices(tag_list)
        for chosen_tag in choice_list:
            remove_file_from_tags([chosen_tag], filename)
    else:
        error_alert("No tags found for given file: {f}".format(f=filename))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-f", "--filename", help="filename to remove tag(s) from")
    group.add_argument("-t", "--tag", help="tag to remove filename(s) from")

    args = parser.parse_args()
    if (args.filename or args.tag) is None:
        parser.error("Must specify either --filename or --tag")

    if args.tag is not None:
        remove_files_from_tag(args.tag.strip())

    elif args.filename is not None:
        remove_tags_from_filename(args.filename.strip())

