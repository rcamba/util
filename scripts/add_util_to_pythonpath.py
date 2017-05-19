import os


def set_persistent_pypath_env_var(new_python_path_env_var):
    os.system("setx PYTHONPATH " + new_python_path_env_var)
    print "If running in cmd, note that environment variables won't take effect until you open a new instance of cmd"


if __name__ == "__main__":

    path_to_module = os.path.dirname(__file__)
    util_resources_dir = os.path.abspath(os.path.join(path_to_module, os.pardir, "util_resources"))

    python_path_env = os.environ.get("PYTHONPATH")

    util_resources_env_str = os.path.realpath(util_resources_dir) + os.pathsep
    if python_path_env is None:
        print "PYTHONPATH environment variable not found. Creating new PYTHONPATH environment variable."
        set_persistent_pypath_env_var(util_resources_env_str)

    elif os.path.realpath(util_resources_dir) not in [os.path.realpath(p) for p in python_path_env.split(os.pathsep)]:
        print "PYTHONPATH environment variable found without util_resources directory. \n" \
              "Appending util_resources directory to PYTHONPATH environment variable."

        if os.environ["PYTHONPATH"][-1] != os.pathsep:  # add separator if there isn't one at the end
            os.environ["PYTHONPATH"] += os.pathsep

        os.environ["PYTHONPATH"] += util_resources_env_str
        set_persistent_pypath_env_var(os.environ["PYTHONPATH"])

    else:
        print util_resources_dir + " is already in PYTHONPATH"
