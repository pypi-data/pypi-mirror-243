"""
confrun.py
"""
import os


def locate_file(start_path: str, file_name: str) -> str:
    """
    locate filename and return absolute file path.
    searching will be recursive upward until system root dir.

    :param file_name: target locate file name
    :param start_path: start locating path, maybe file path or directory path
    """
    if os.path.isfile(start_path):
        start_dir_path = os.path.dirname(start_path)
    elif os.path.isdir(start_path):
        start_dir_path = start_path
    else:
        raise FileExistsError(f"invalid path: {start_path}")

    file_path = os.path.join(start_dir_path, file_name)
    if os.path.isfile(file_path):
        # ensure absolute
        return os.path.abspath(file_path)

    # system root dir
    # Windows, e.g. 'E:\\'
    # Linux/Darwin, '/'
    parent_dir = os.path.dirname(start_dir_path)
    if parent_dir == start_dir_path:
        raise FileExistsError(f"{file_name} not found in {start_path}")

    # locate recursive upward
    return locate_file(parent_dir, file_name)


def locate_confrun_py(start_path: str) -> str:
    """
    locate confrun.py file

    :param start_path: start locating path,
        maybe testcase file path or directory path
    """
    try:
        # locate debugtalk.py file.
        confrun_path = locate_file(start_path, "confrun.py")
    except FileExistsError:
        confrun_path = None

    return confrun_path
