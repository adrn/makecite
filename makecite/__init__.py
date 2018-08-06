#!/usr/bin/env python
import os
import os.path
import sys
from makecite.discover import find_all_files

__version__ = "0.0.1"


def main():
    current_path = None
    if len(sys.argv)>1 and os.path.exists(sys.argv[-1]) :
        current_path = sys.argv[-1]
    print(find_all_files(current_path))


if __name__ == '__main__':
    main()
