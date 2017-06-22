from get_newest_file import add_arg_options, get_newest_file

if __name__ == "__main__":
    parser = add_arg_options()
    args = parser.parse_args()
    get_newest_file(args)
