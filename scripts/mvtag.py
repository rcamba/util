from tag_rename import tag_rename
from sys import argv


if __name__ == "__main__":
    tag_rename(argv[1], argv[2], verbose=True, allow_empty_tags=False)
