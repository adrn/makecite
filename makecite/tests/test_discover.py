"""Testing the discovery of python and ipython notebook files
"""

import os

from makecite import discover
import makecite

def test_discover():
    """Test finding the files in the module's directory"""
    bpath = os.path.dirname(os.path.abspath(makecite.__file__))
    discovered = discover.find_all_files(bpath)
    assert 'discover.py' in [x.split('/')[-1] for x in discovered['.py']]
    assert  '__init__.py' in [x.split('/')[-1] for x in discovered['.py']]
    assert 'test_discover.py'in [x.split('/')[-1] for x in discovered['.py']]
