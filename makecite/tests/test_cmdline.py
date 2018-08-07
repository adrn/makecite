# Standard library
from os import path

# Third party
import pytest

# Package
from ..cmdline import get_all_packages, get_bibtex, main

_path = path.join(path.split(path.abspath(__file__))[0], 'data')


def test_readme_examples():
    # makecite my_script.py
    pkgs = get_all_packages(path.join(_path, 'file1.py'))
    expected_pkgs = ['os', 'sys']
    assert all([x in pkgs for x in expected_pkgs])

    # makecite --ext=.py .
    pkgs = get_all_packages(_path, extensions=['.py'])
    expected_pkgs = ['os', 'sys', 'pickle', 're', 'datetime']
    assert all([x in pkgs for x in expected_pkgs])

    # makecite --ext=.py --ext=.ipynb my_code my_notebooks
    pkgs = get_all_packages(
        [path.join(_path, 'other_scripts/moar_stuff'),
         path.join(_path, 'other_scripts/even_moar_stuff')],
        extensions=['.py', '.ipynb'])
    expected_pkgs = ['os', 'sys', 're', 'pickle', 'datetime']
    assert all([x in pkgs for x in expected_pkgs])


def test_bibtex():

    bibtex = get_bibtex('astropy')
    assert isinstance(bibtex, str)

    with pytest.raises(ValueError):
        get_bibtex('some_fake_package')


def test_cli():
    main({'paths': _path})


def test_failures():

    with pytest.raises(ValueError):
        get_all_packages(_path, extensions=['.py', '.rst'])
