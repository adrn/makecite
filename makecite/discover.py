"""makecite.discover: Discover all imports used in all python files in the current folder.
"""
import os
from os.path import expanduser, abspath, join

def find_all_files(root_path=None, extensions=['.py', '.ipynb']):
    """Find all relevant files in the current directory
    and returns a dictionary, grouping files by type (.ipynb, .py)

    Parameters
    ----------
    root_path : str, optional
        The path where to search for the python files. (Default:None => From
        current pwd).

    Returns
    -------
    files : dict
        A dictionary with keys = file extensions
    """
    if not root_path:
        root_path = os.path.abspath(os.getcwd())

    root_path = expanduser(root_path)

    # Set up container to store all files with the requested extensions
    _files = {}
    for ext in extensions:
        _files[ext] = []

    for root, _, files in os.walk(root_path):
        for _file in files:
            _, ext = os.path.splitext(_file)
            if ext in extensions:
                _files[ext].append(abspath(join(root, _file)))

    return _files
