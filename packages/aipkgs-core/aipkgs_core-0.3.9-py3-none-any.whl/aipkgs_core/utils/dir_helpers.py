import os
import pathlib
import shutil


class PathType:
    isPath = 0
    isDirectory = 1
    isFile = 2


def check_path_type(path):
    if os.path.isdir(path):
        return PathType.isDirectory
    elif os.path.isfile(path):
        return PathType.isFile
    else:
        return PathType.isPath


def directory_is_accessible(path):
    if (check_path_type(path) is PathType.isDirectory) and os.access(path, os.R_OK):
        return True
    else:
        return False


def create_dir(path: str):
    path = pathlib.Path(path)
    if directory_is_accessible(path):
        pass
    else:
        try:
            os.mkdir(path)
        except OSError:
            print("Creation of the directory %s failed" % path)
        else:
            print("Successfully created the directory %s " % path)

    return path


def create_dirs(path: str):
    path = pathlib.Path(path)
    if directory_is_accessible(path):
        pass
    else:
        try:
            os.makedirs(path)
        except OSError:
            print("Creation of the directory %s failed" % path)
        else:
            print("Successfully created the directory %s " % path)

    return path


def remove_dir(path: str):
    try:
        shutil.rmtree(path)
    except OSError as e:
        print(f'path: {path} could not be deleted')
