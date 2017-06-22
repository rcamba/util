from sys import argv
from os import getcwd, path
from win32com import client


def get_folder_size(folder_path):

    if path.isdir(folder_path):

        fso = client.Dispatch("Scripting.FileSystemObject")
        folder = fso.GetFolder(folder_path)
        mb = 1024 * 1024.0
        print "%.2f MB" % (folder.Size / mb)

    else:
        print folder_path, " is not a valid or accessible directory."


if __name__ == "__main__":
    if len(argv) == 2:
        get_folder_size(argv[1])
    else:
        get_folder_size(getcwd())
