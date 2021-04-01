import os
import shutil


from file_manager.exceptions import *
import config as config


ROOT_DIR = os.path.abspath(config.ROOT_DIR)
CUR_DIR = []


def get_dir(*paths, check_exist=True):
    """
    Checks if directory exists and available
    :param paths: collected path segments
    :param check_exist: if True, checks existing and type
    :return: path to directory
    """
    abs_path = os.path.abspath(os.path.join(ROOT_DIR, *CUR_DIR, *paths))
    if check_exist:
        if not os.path.exists(abs_path):
            raise DirNotExistsException(os.path.join(*CUR_DIR, *paths))
        if not os.path.isdir(abs_path):
            raise NotDirException(os.path.join(*CUR_DIR, *paths))
    if ROOT_DIR != abs_path[:len(ROOT_DIR)]:
        raise PassThrowRootException
    return abs_path


def get_file(*paths, check_exist=True):
    """
    Checks if file exists and available
    :param paths: collected path segments
    :param check_exist: if True, checks existing and type
    :return: path to file
    """
    abs_path = os.path.abspath(os.path.join(ROOT_DIR, *CUR_DIR, *paths))
    if check_exist:
        if not os.path.exists(abs_path):
            raise FileNotExistsException(os.path.join(*CUR_DIR, *paths))
        if not os.path.isfile(abs_path):
            raise NotFileException(os.path.join(*CUR_DIR, *paths))
    if ROOT_DIR != abs_path[:len(ROOT_DIR)]:
        raise PassThrowRootException
    return abs_path


def command(cmd):
    """
    Decorator
    Executes command
    Catches standard errors end returns them
    :param cmd: function for wrapping
    :return: wrapped function
    """
    def wrap(*args, flags=None):
        try:
            return cmd(*args, flags=flags)
        except PassThrowRootException:
            return "Can't across root dir"
        except (FileNotExistsException, FileNotFoundError) as e:
            return "Can't find file " + e.args[0]
        except DirNotExistsException as e:
            return "Can't find directory " + e.args[0]
        except NotDirException as e:
            return "Isn't a directory " + e.args[0]
        except NotFileException as e:
            return "Isn't a file " + e.args[0]
    return wrap


@command
def echo(text="", flags=None):
    return text


@command
def pwd(flags=None):
    return "~" + (os.sep if len(CUR_DIR) > 0 else "") + os.sep.join(CUR_DIR)


@command
def dir_list(folder=None, flags=None):
    if folder is None:
        dirs = "\n".join(os.listdir(get_dir()))
    else:
        dirs = "\n".join(os.listdir(get_dir(folder)))
    if dirs != "":
        return dirs


@command
def touch(*file_names, flags=None):
    for file_name in file_names:
        file_path = get_file(file_name, check_exist=False)
        if os.path.exists(file_path):
            return "File already exists"
        else:
            open(file_path, "w").close()


@command
def make_dir(*dir_names, flags=None):
    for dir_name in dir_names:
        try:
            dir_path = get_dir(dir_name, check_exist=False)
            os.mkdir(dir_path)
        except FileExistsError:
            return "Directory already exists"


@command
def remove(*file_names, flags=None):
    for file_name in file_names:
        file_path = get_file(file_name)
        os.remove(file_path)


@command
def remove_dir(*dir_names, flags=None):
    for dir_name in dir_names:
        dir_path = get_dir(dir_name)
        if "-r" in flags:
            shutil.rmtree(dir_path)
        elif len(os.listdir(dir_path)) == 0:
            shutil.rmtree(dir_path)
        else:
            return "Directory isn't empty"


@command
def change_dir(dir_name="..", flags=None):
    global CUR_DIR
    new_dir = get_dir(dir_name)
    CUR_DIR = new_dir[len(ROOT_DIR) + 1:].split(os.sep)


@command
def write(text, file_name, flags=None):
    if "-a" in flags:
        file = open(get_file(file_name), "a")
    else:
        file = open(get_file(file_name, check_exist=False), "w")
    file.write(text)
    file.close()


@command
def read(file_name, flags=None):
    with open(get_file(file_name), "r") as file:
        return "".join(file.readlines())


@command
def copy(src, dest, flags=None):
    shutil.copy(get_file(src), get_dir(dest, check_exist=False))


@command
def move(src, dest, flags=None):
    shutil.move(get_file(src), get_dir(dest, check_exist=False))


@command
def rename(src, dest, flags=None):
    os.rename(get_dir(src, check_exist=False), get_dir(dest, check_exist=False))
