def parse_py_module(filename):
    """A simple parser for extracting the names of imported modules / packages
    from a Python module.

    Parameters
    ----------
    filename : str
        Path to a Python module.

    Notes
    -----
    - This currently fails to parse multi-line imports that use "\"! For example

        import astropy, \
        numpy

      but that seriously violates PEP8 anyways!

    """
    with open(filename, 'r') as f:
        all_packages = []
        for line in f:
            line = line.rstrip('\n')

            if line.startswith('import'):
                line = line[7:]

            elif line.startswith('from'):
                line = line[5:]

            else:
                continue

            line = line.split(' as ')[0]
            line = line.split(' import ')[0]

            if ',' in line:
                line = [x.strip() for x in line.split(',')]

            else:
                line = [line]

            all_packages += line

    return set(all_packages)
