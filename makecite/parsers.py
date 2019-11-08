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

    """
    if path.exists(filename_or_str):
        with open(filename_or_str, 'r') as _file:
            lines = _file.readlines()

    else:
        lines = filename_or_str.split('\n')

    all_packages = []
    for line in lines:
        line = line.rstrip('\n')

        if line.startswith('import'):
            parsed_line = line[7:]

        elif line.startswith('from'):
            parsed_line = line[5:]

        else:
            continue

        packages = parsed_line.split(' as ')[0]
        packages = packages.split(' import ')[0]

        # Split up import statements with multiple packages, comma-separated
        if ',' in packages and '\\' not in packages:
            packages = [x.strip() for x in packages.split(',')]

        elif ',' in packages and "\\" in packages:
            packages = [x.strip() for x in packages.split(',')][:-1]
            next_packages = lines[lines.index(line+'\n')+1].strip()

            if ',' in next_packages:
                for pkg in next_packages.split(','):
                    packages.append(pkg)
            else:
                packages.append(next_packages)

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

    with open(filename) as _file:
        nb_stuff = nbformat.reads(_file.read(), as_version=4)

    exporter = PythonExporter()
    (body, _) = exporter.from_notebook_node(nb_stuff)

    return parse_py_module(body)


parser_map = {'.py': parse_py_module,
              '.pyx': parse_py_module,
              '.ipynb': parse_ipynb_file}
