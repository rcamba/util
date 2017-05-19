"""
Used with scripts/ql.bat, qla.bat, and qlb.bat
ql reads from the jump file and changes to the directory written at the top of that file
qla adds curr dir to list
qlb just back to previous dir; similar to pushd . and popd
Required to do it from cmd/bat since python process is separate from cmd
"""
from argparse import ArgumentParser
from string import strip
from os import getcwd
from root import dir_jump_file_log, print_list, choose_from_list, prev_dir_log, create_back_up


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
    del jump_list[targ_pos]  # del apparently more efficient than pop; avoids issue where directory is also prevDir

    create_back_up(dir_jump_file_log)
    write_to_dir_jump(jump_list)


def write_to_dir_jump(flist):

    with open(dir_jump_file_log, "w") as out:
        for f in flist:
            out.write(f)
            out.write("\n")


def get_jump_list():
    with open(dir_jump_file_log, "r") as f:
        lines = f.readlines()
        lines = map(strip, lines)

    return lines


if __name__ == "__main__":
    parser = ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("jump_index", type=int, nargs='?', help="number index of directory to change directory in to")
    group.add_argument("-a", "--add-dir", action="store_true", help="add a directory to list")
    group.add_argument("-d", "--delete-dir", type=int, help="delete a directory from list")

    args = parser.parse_args()

    if args.add_dir:
        add_to_dir_jump(getcwd())

    elif args.delete_dir:
        remove_from_dir_jump(args.delete_dir)

    elif args.jump_index is not None:
        sort_dir_jump(args.jump_index)

    else:
        jumpList = get_jump_list()
        print_list(jumpList[1:])
        choice = choose_from_list(jumpList[1:])  # +1 for skipping first line of jumped route
        sort_dir_jump(jumpList.index(choice))
