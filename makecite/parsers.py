from os import path

def parse_py_module(filename_or_str):
    """A simple parser for extracting the names of imported modules / packages
    from a Python module.

    Parameters
    ----------
    filename_or_str : str
        Path to a Python module, or text read from a Python module.

    Returns
    -------
    packages : set
        A unique list of all (root) packages imported by the specified notebook
        file.

    Notes
    -----
    - This currently fails to parse multi-line imports that use "\"! For example

        import astropy, \
        numpy

      but that seriously violates PEP8 anyways!

    """
    if path.exists(filename_or_str):
        with open(filename_or_str, 'r') as f:
            lines = f.readlines()

    else:
        lines = filename_or_str.split('\n')

    all_packages = []
    for line in lines:
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
    """A simple parser for extracting the names of imported modules / packages
    from an IPython (Jupyter) notebook.

    Parameters
    ----------
    filename : str
        Path to an IPython notebook file.

    Returns
    -------
    packages : set
        A unique list of all (root) packages imported by the specified notebook
        file.

    """
    import nbformat
    from nbconvert import PythonExporter

    with open(filename) as f:
        nb_stuff = nbformat.reads(f.read(), as_version=4)

    exporter = PythonExporter()
    (body, resources) = exporter.from_notebook_node(nb_stuff)

    return parse_py_module(body)


parser_map = {'.py': parse_py_module,
              '.ipynb': parse_ipynb_file}
