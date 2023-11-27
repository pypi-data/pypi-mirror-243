# Nov-26-2023
# utils.py

from pathlib import Path


def init_directory(dir_name):

    path_dir = Path.cwd() / dir_name

    if path_dir.is_dir():
        for child in path_dir.glob('*'):
            if child.is_file():
                child.unlink()
    else:
        create_directory(dir_name)


def create_directory(dir_name):

    path_dir = Path.cwd() / dir_name

    if not path_dir.is_dir():
        path_dir.mkdir()


def remove_directory(dir_name):

    path_dir = Path.cwd() / dir_name

    if path_dir.is_dir():
        for child in path_dir.glob('*'):
            if child.is_file():
                child.unlink()
        path_dir.rmdir()
