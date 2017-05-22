if __name__ == "__main__":
    from search_tags import search, set_args, create_args, parse_args

    parser = create_args()
    args = parse_args(parser)

    set_args(args)
    search(args.tags, args.exception_tags)
