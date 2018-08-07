import os
import makecite

import sys, os
myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')
from makecite import discover

def test_discover():
    bpath = os.path.dirname(os.path.abspath(makecite.__file__))
    discovered = discover.find_all_files(bpath) 
    assert 'discover.py' in discovered['py']
    assert  '__init__.py' in discovered['py']
    assert 'test_discover.py'in discovered['py']

