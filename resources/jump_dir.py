"""
Used with ql.bat
QL reads from the jump file and changes to the directory written in that file
Required to do it from cmd/bat since python process is separate from cmd
"""
from root import dir_jump_file_log, print_list, choose_from_list, prev_dir_log, \
    switch_parser, create_back_up, error_alert
from sys import argv
from string import strip
from os import getcwd


AVAILABLE_SWITCHES = ['a', 'd']


def write_to_prev_dir_file(prev_dir):

    with open(prev_dir_log, "w+") as f:
        f.write(prev_dir)


def sort_dir_jump(targ_pos):

    jump_list = get_jump_list()
    jump_list[0] = jump_list[targ_pos]
    write_to_prev_dir_file(getcwd())
    write_to_dir_jump(jump_list)


def add_to_dir_jump(targ_dir):

    create_back_up(dir_jump_file_log)
    print "Adding: " + targ_dir
    with open(dir_jump_file_log, "a") as f:
        f.write(str(getcwd()))


def remove_from_dir_jump(targ_pos):

    jump_list = get_jump_list()
    print "Removing: " + jump_list[targ_pos]
    jump_list.remove(jump_list[targ_pos])
    create_back_up(dir_jump_file_log)
    write_to_dir_jump(jump_list)


def write_to_dir_jump(flist):

    with open(dir_jump_file_log, "w") as out:
        for f in flist:
            out.write(f)
            out.write("\n")


def get_jump_list():

    lines = []
    with open(dir_jump_file_log, "r") as f:
        lines = f.readlines()
        lines = map(strip, lines)

    return lines

if __name__ == "__main__":

    switches = switch_parser(argv)
    if 'a' in switches:
        add_to_dir_jump(getcwd())

    elif 'd' in switches:
        try:
            targ_pos = int(switches['d'])
        except ValueError:
            error_alert(
                "-d must contain int for dir to be deleted from jump list")
        remove_from_dir_jump(targ_pos)

    elif len(argv) > 1:
        try:
            targ_pos = int(argv[1])
        except ValueError:
            error_alert("# out of directory listing", True)
        sort_dir_jump(targ_pos)

    else:
        jumpList = get_jump_list()
        print_list(jumpList[1:])
        choice = choose_from_list(jumpList[1:])
        # +1 for skipping first line of jumped route
        sort_dir_jump(jumpList.index(choice))
