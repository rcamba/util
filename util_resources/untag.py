from tag import remove_file_from_tags, get_tags_for_file, get_files_from_tags
from sys import argv
from root import print_list, switch_parser, key_press_input

AVAILABLE_SWITCHES = ['f', 't']


def _choose_from_list(tag_or_file_list):

    choice_list = []
    if len(tag_or_file_list) > 1:
        print "Enter number(s) separated by commas"

        try:
            _input = raw_input()
        except EOFError:  # pipes
            _input = key_press_input()

        choices = _input.split(',')
        choices = map(int, choices)

        for choice in choices:
            choice_list.append(tag_or_file_list[choice - 1])

    else:
        choice_list.append(tag_or_file_list[0])

    return choice_list


def untag_using_tag(tag):

    f_list = get_files_from_tags(tag)
    if len(f_list) > 0:
        print_list(f_list)
        choice_list = _choose_from_list(f_list)
        for choiceFile in choice_list:
            remove_file_from_tags([tag], choiceFile)


def untag_using_filename(filename):

    tag_list = get_tags_for_file(filename)
    if len(tag_list) > 0:
        print_list(tag_list)
        choice_list = _choose_from_list(tag_list)
        for choiceTag in choice_list:
            remove_file_from_tags([choiceTag], filename)


if __name__ == "__main__":

    switches = switch_parser(argv, AVAILABLE_SWITCHES)

    if len(argv) > 1 and ('t' in switches or 'f' in switches):

        if 't' in switches:
            untag_using_tag(argv[1].strip())

        elif 'f' in switches:
            untag_using_filename(argv[1].strip())
    else:
        print "Invalid parameters"
        print "Usage untag[-f filename][-t tag]"
