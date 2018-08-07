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

            packages = line.split(' as ')[0]
            packages = packages.split(' import ')[0]

            # Split up import statements with multiple packages, comma-separated
            if ',' in packages:
                packages = [x.strip() for x in packages.split(',')]

            else:
                packages = [packages]

            # Extract the root package name from imported subpackages and
            # remove relative imports, dunder imports (like __future__)
            packages = [pkg.split('.')[0] for pkg in packages
                        if not pkg.startswith('.') and not pkg.startswith('__')]

            all_packages += packages

    return set(all_packages)


def parse_ipynb_file(filename):
    """ """
    pass


parser_map = {'.py': parse_py_module,
              '.ipynb': parse_ipynb_file}
