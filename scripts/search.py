"""
Using .py because .bat reads commas as a separator/delimiter
"""

if __name__ == "__main__":
    from search_tags import create_args, do_search

    parser = create_args()
    do_search(parser)
