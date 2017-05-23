if __name__ == "__main__":
    from search_tags import create_args, parse_args, do_search

    parser = create_args()
    args = parse_args(parser)
    do_search(args)
