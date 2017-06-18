import os
import time
import _winreg


"""
Create/Append user environment variables

var_name: var_value

PYTHONPATH: Util\util_resources;
PATH: Util\scripts;
Util: Util
"""


def write_curr_env_vars(env_name):
    with open('env_vars.txt', 'a') as writer:
        writer.write("{time_}: {env} = {env_val}".format(
            time_=time.strftime("%b %d, %H:%M", time.localtime()),
            env=env_name, env_val=str(get_user_environ_var(env_name))))
        writer.write("\n" * 2)


# https://stackoverflow.com/a/23624136
def set_persistent_env_var(env_var_name, env_var_val):
    write_curr_env_vars(env_var_name)
    set_reg(env_var_name, env_var_val)


def get_user_environ_var(var_name):
    try:
        registry_key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, "Environment", 0,
                                       _winreg.KEY_READ)
        value, regtype = _winreg.QueryValueEx(registry_key, var_name)
        _winreg.CloseKey(registry_key)
        return value
    except WindowsError:
        return None


def set_reg(var_name, value):
    try:
        _winreg.CreateKey(_winreg.HKEY_CURRENT_USER, "Environment")
        registry_key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, "Environment", 0,
                                       _winreg.KEY_WRITE)
        _winreg.SetValueEx(registry_key, var_name, 0, _winreg.REG_SZ, value)
        _winreg.CloseKey(registry_key)
        return True
    except WindowsError:
        return False


def start_setting_env_var(env_name, env_path, fail_if_already_exists=False):
    print "Path to be added:", env_path

    existing_env_vals = get_user_environ_var(env_name)

    env_path_str = os.path.realpath(env_path)

    if not fail_if_already_exists:  # if the env var can have more than one item then have separators
        env_path_str += os.pathsep

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

            user_env_var = get_user_environ_var(env_name)
            if user_env_var[-1] != os.pathsep:  # add separator if there isn't one at the end
                user_env_var += os.pathsep

            user_env_var += env_path_str
            set_persistent_env_var(env_name, user_env_var)

    else:
        print "{p} is already in {e}\n".format(e=env_name, p=env_path)


def check_for_name_conflicts(targ_folder):
    """
    where.exe

    check for name conflicts based on items in PATH environment variable

    alt to parsing result from
        map(lambda f: subprocess.Popen(["where", f], stdout=subprocess.PIPE, shell=True).communicate()[0],
        [t for t in os.listdir(target_folder)])

    :param targ_folder: folder to check against
    :return:
    """

    valid_exts = os.getenv("PATHEXT").split(os.pathsep)  # PATHEXT is sys env variable
    valid_exts = map(lambda v: v.lower(), valid_exts)

    env_paths = os.getenv("PATH").split(os.pathsep)  # get both sys and user env variable
    env_paths = [os.path.realpath(e).lower() for e in env_paths]
    env_paths = list(set(env_paths))

    targ_folder = os.path.realpath(targ_folder).lower()

    if targ_folder in env_paths:
        env_paths.remove(targ_folder)

    env_path_files_dict = {}
    for p in env_paths:
        if not os.path.isdir(p):
            pass
            # if verbose:
            #     print "{d} is not a valid directory in your PATH environment variable".format(d=p)
        else:
            env_path_files_dict[p] = os.listdir(p)

    targ_folder_f_list = os.listdir(targ_folder)
    for k in env_path_files_dict.iterkeys():
        for t in targ_folder_f_list:
            if os.path.isfile(os.path.join(targ_folder, t)):
                t_no_ext = os.path.splitext(t)[0]
                for f in env_path_files_dict[k]:
                    if os.path.splitext(f)[1].lower() in valid_exts:
                        f_no_ext = os.path.splitext(f)[0]
                        if t_no_ext == f_no_ext:
                            print "Name collision:", t
                            print "\t", os.path.join(targ_folder, t)
                            print "\t", os.path.join(k, f)


if __name__ == "__main__":
    path_to_module = os.path.dirname(__file__)

    pypath_env_name = "PYTHONPATH"
    pypath_env_path = os.path.realpath(os.path.join(path_to_module, "util_resources"))
    start_setting_env_var(pypath_env_name, pypath_env_path)

    util_env_name = "Util"
    util_env_path = os.path.realpath(path_to_module)
    start_setting_env_var(util_env_name, util_env_path, fail_if_already_exists=True)

    path_env_name = "PATH"
    path_env_value = os.path.realpath(os.path.join(util_env_path, "scripts"))
    start_setting_env_var(path_env_name, path_env_value)

    py_io_encoding = "PYTHONIOENCODING"
    curr_pyioencoding_val = get_user_environ_var(py_io_encoding)
    if curr_pyioencoding_val is None:
        print "Creating {} with {}".format(py_io_encoding, "utf-8")
        set_persistent_env_var(py_io_encoding, "utf-8")
    else:
        print "PYTHONIOENCODING is already set to", curr_pyioencoding_val

    print "\nIf running in cmd, " \
          "note that environment variables won't take effect until you open a new instance of cmd\n"

    check_for_name_conflicts(path_env_value)
