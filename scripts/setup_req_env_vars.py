import os


def set_persistent_env_var(env_var_name, env_var_val):
    command = "setx {env_name} {env_var}".format(env_name=env_var_name, env_var=env_var_val)
    print "Executing:", command
    os.system(command)
    print "If running in cmd, note that environment variables won't take effect until you open a new instance of cmd\n"


def start_setting_env_var(env_name, env_path, fail_if_already_exists=False):
    print "Path to be added:", env_path

    existing_env_vals = os.environ.get(env_name)

    env_path_str = os.path.realpath(env_path) + os.pathsep
    if existing_env_vals is None:
        print "{e} environment variable not found. Creating new {e} environment variable.".format(e=env_name)
        set_persistent_env_var(env_name, env_path_str)

    elif os.path.realpath(env_path) not in [os.path.realpath(p) for p in existing_env_vals.split(os.pathsep)]:
        if fail_if_already_exists:  # only one value allowed for the env_var
            raise Exception("{e} environment variable already exists which should only be one value."
                            "\nContents:{c}".format(e=env_name, c=str(existing_env_vals.split(os.pathsep))))
        else:
            print ("{e} environment variable found without {p}.\n"
                   "Appending {p} to {e} environment variable.").format(e=env_name, p=env_path)

            if os.environ[env_name][-1] != os.pathsep:  # add separator if there isn't one at the end
                os.environ[env_name] += os.pathsep

            os.environ[env_name] += env_path_str
            set_persistent_env_var(env_name, os.environ[env_name])

    else:
        print "{p} is already in {e}".format(e=env_name, p=env_path)


if __name__ == "__main__":
    path_to_module = os.path.dirname(__file__)

    pypath_env_name = "PYTHONPATH"
    pypath_env_path = os.path.realpath(os.path.join(path_to_module, os.pardir, "util_resources"))
    start_setting_env_var(pypath_env_name, pypath_env_path)

    util_env_name = "Util"
    util_env_path = os.path.abspath(os.path.join(path_to_module, os.pardir))
    start_setting_env_var(util_env_name, util_env_path, fail_if_already_exists=True)


