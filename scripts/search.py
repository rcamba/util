if __name__ == "__main__":
    from sys import argv, path as sys_path
    from os import path as os_path
    path_to_module = os_path.dirname(__file__)
    resources_path = os_path.join(path_to_module, "resources")
    sys_path.insert(0, resources_path)
    from search_tags import main

    main(argv[1:])

