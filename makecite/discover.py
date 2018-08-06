"""makecite.discover: Discover all imports used in all python files in the current folder. 
"""
import os
from os.path import expanduser
from os import walk

def find_all_files(root_path=None):
    """Find all relevant files in the current directory 
    and returns a dictionary, grouping files by type (.ipynb, .py)

    :param root_path: The path where to search for the python files 
                    (Default:None=> From current pwd)
    :type root_path: str
    :return: dictionary with keys = file extensions
    :rtype: dict
    """
    if not root_path: 
        root_path = os.getcwd()
    root_path = expanduser(root_path)
    _files={'py':[], 'ipynb':[]}
    for root, dirs, files in os.walk(root_path):
        for _file in files:
            for ext in list(_files):
                if _file.endswith("."+ext):
                    _files[ext].append(_file)
    return _files




