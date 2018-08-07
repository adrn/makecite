# Standard library
from os import path

# Third party
import pytest

# Package
from ..cmdline import get_all_packages

_path = path.split(path.abspath(__file__))[0]


def test_readme_examples():
    # makecite my_script.py
    pkgs = get_all_packages(path.join(_path, 'data/file1.py'))
    expected_pkgs = ['os', 'sys']
    assert all([x in pkgs for x in expected_pkgs])

    # makecite --ext=.py .
    pkgs = get_all_packages(path.join(_path, 'data/'),
                            extensions=['.py'])
    expected_pkgs = ['os', 'sys', 'pickle', 're', 'datetime']
    assert all([x in pkgs for x in expected_pkgs])

    # makecite --ext=.py --ext=.ipynb my_code my_notebooks
    pkgs = get_all_packages(
        [path.join(_path, 'data/other_scripts/moar_stuff'),
         path.join(_path, 'data/other_scripts/even_moar_stuff')],
        extensions=['.py', '.ipynb'])
    expected_pkgs = ['os', 'sys', 're', 'pickle', 'datetime']
    assert all([x in pkgs for x in expected_pkgs])


def test_failures():

    with pytest.raises(ValueError):
        get_all_packages(path.join(_path, 'data/'),
                         extensions=['.py', '.rst'])
