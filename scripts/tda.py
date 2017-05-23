from sys import argv
from to_do_list import add_item


if __name__ == "__main__":
    if len(argv) > 1:
        add_item(" ".join(argv[1:]))
    else:
        task = raw_input("\nEnter task argument: ")
        if len(task) > 1:
            add_item(task)
