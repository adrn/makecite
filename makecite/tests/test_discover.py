import os
import makecite
from makecite import discover

def test_discover():
    bpath = os.path.dirname(os.path.abspath(makecite.__file__))
    discovered = discover.find_all_files(bpath) 
    assert 'discover.py' in discovered['py']
    assert  '__init__.py' in discovered['py']
    assert 'test_discover.py'in discovered['py']

