"""Read file from disk and return file object"""

from pathlib import Path


def get_file_format(filepath):
    """Returns file extension without dot"""
    return Path(filepath).suffix[1:]


def open_file_if_exists(filepath, encoding='utf-8', filemode='r'):
    path = Path(filepath)

    if path.is_file():
        return open(filepath, encoding=encoding, mode=filemode)
    else:
        raise ValueError(f"File doesn't exist at {filepath}")

