# Standard library
import os
import re
import sys
import warnings
import importlib
from cffconvert import Citation

# Package
from . import __version__
from .discover import find_all_files
from .parsers import parser_map

_bib_path = os.path.join(os.path.split(os.path.abspath(__file__))[0],
                         'bibfiles')
cite_tag_pattr = re.compile('@[a-zA-Z]+\{(.*),')



def get_all_packages(paths, extensions=['.py', '.ipynb'],
                     include_imported_dependencies=False):
    """Get a unique list (set) of all package names imported by all files of
    the requested extensions

    Parameters
    ----------
    paths : list, str
    extensions : list, iterable
    include_imported_dependencies : bool, optional

    Returns
    -------
    packages : set

    """
    if isinstance(paths, str):
        paths = [paths]

    all_packages = set()
    for path in paths:
        if os.path.isfile(path):
            basename, ext = os.path.splitext(path)
            file_dict = {ext: [path]}

        else:
            file_dict = find_all_files(path, extensions=extensions)

        for ext, files in file_dict.items():
            if ext not in parser_map:
                raise ValueError('File extension "{0}" is not supported.'
                                 .format(ext))

            for file in files:
                _packages = parser_map[ext](file)
                all_packages = all_packages.union(_packages)

    if include_imported_dependencies:
        init_modules = sys.modules.copy()

        # Now we have a list of package names, so we can import them and track
        # what other packages are imported as dependencies. If requested, we add
        # those to the package list as well
        for package_name in all_packages:
            try:
                importlib.import_module(package_name)
            except ImportError:
                # here, just skip if we can't import: a warning is issued later
                pass

        loaded_modules = sys.modules.copy()
        diff_modules = set(loaded_modules.keys()) - set(init_modules.keys())

        additional_modules = set()
        for module in diff_modules:
            top_level = module.split('.')[0]

            if top_level.startswith('_'):
                continue

            additional_modules.add(top_level)

        all_packages = all_packages.union(additional_modules)

    return all_packages


def get_bibtex(package_name):
    """Fetch the bibtex entry for the specified package by comparing to our
    local list of bibtex entries.

    Parameters
    ----------
    package_name : str

    Returns
    -------
    bibtex : str

    """
    full_path = os.path.join(_bib_path, '{0}.bib'.format(package_name.lower()))
    if not os.path.exists(full_path):
        raise ValueError('Bibtex not found for {0}! If you know it has a '
                         'citation, please consider adding it via pull request '
                         ' to: https://github.com/adrn/makecite')

    with open(full_path, 'r') as f:
        bibtex = f.read()

    return bibtex


def get_bibtex_from_package(package_name, update_local=False):
    """
    Fetch BibTeX information directly from the package if available either via
    __bibtex__ or __citation__.

    Parameters
    ----------
    package_name : str
        Name of the package.
    update_local : bool
        If True, update the local BibTeX information in ``makecite``. Default is False.

    Returns
    -------
    bibtex : str or None
        Returns the BibTeX string or None if the package is not installed or doesn't provide one.
    """
    try:
        package = importlib.import_module(package_name)
        for attr in ['__bibtex__', '__citation__']:
            citation_info = getattr(package, attr, None)
            if citation_info:
                break
    except ImportError:
        warnings.warn(f"{package_name} is not installed, cannot look for "
                      "package provided BibTeX.")
        return None

    if citation_info and update_local:
        path = os.path.join(_bib_path, '{0}.bib'.format(package_name))
        with open(path, 'w') as f:
            f.write(citation_info)

    return citation_info


def get_bibtex_from_citation_file(package_name):
    """
    Fetch BibTeX information directly from the package if available in either
    of the files CITATION.cff or CITATION (if installed).

    Parameters
    ----------
    package_name : str
        Name of the package.

    Returns
    -------
    bibtex : str or None
        Returns the BibTeX string or None if the package is not installed or doesn't provide one.
    """
    package = importlib.import_module(package_name)
    cff_file = os.path.join(package.__path__[0], 'CITATION.cff')
    citation_file = os.path.join(package.__path__[0], 'CITATION')
    if os.path.exists(cff_file):
        with open(cff_file) as f:
            cffstr = f.read()
        citation = Citation(cffstr=cffstr)
        bibtex = citation.as_bibtex()
    elif os.path.exists(citation_file):
        with open(citation_file) as f:
            citestr = f.read()
        match = re.search(cite_tag_pattr, citestr)
        if match is None:
            raise ValueError('Could not find any BibTeX entries in CITATION file')
        for i_end in range(match.end(), len(citestr)):
            bibtex = citestr[match.start():i_end]
            if bibtex.count('{') == bibtex.count('}'):
                break
        else:
            raise ValueError('Mismatched braces in BibTeX entry in CITATION file')
    else:
        bibtex = None
    return bibtex


def main(args=None):
    from argparse import ArgumentParser, RawTextHelpFormatter

    examples = '''Get bibtex records for packages used in a single script, and store to a `.bib` file in the current working directory:

    makecite my_script.py


    Get bibtex records for packages used in all `.py` scripts in the current directory and store to a `.bib` file called "software_refs.bib":

    makecite --ext=.py -o software_refs.bib .


    Get bibtex records for packages used in all `.py` scripts and IPython notebook, `.ipynb`, files in two paths `my_code` and `my_notebooks`:

    makecite --ext=.py --ext=.ipynb my_code my_notebooks


    Get bibtex records for packages used in all `.py` scripts in the current directory and output a AAS journals `\software{}` tag:

    makecite --ext=.py --aas .
    '''

    desc = ('(Version {0})\n\n'
            'Generate latex + bibtex citation commands by looking at what '
            'packages are imported in your Python code.\n\n'
            'Examples\n--------\n{1}'.format(__version__, examples))
    parser = ArgumentParser(description=desc,
                            formatter_class=RawTextHelpFormatter)

    parser.add_argument('-e', '--ext', action='append', dest='extensions',
                        default=None,
                        help='Specify the file extensions to look for and '
                             'parse. Currently, only .py and .ipynb are '
                             'supported.')

    parser.add_argument('-o', '--output-file', dest='output_file',
                        default=None,
                        help='For example, "software-refs.bib". The file to '
                             'save the bibtex references to. If the file '
                             'exists, this will append the citations to the ' 'end of the existing file. Otherwise, the file '
                             'is created.')

    parser.add_argument('-r', '--recursive', dest='recursive', default=False,
                        action='store_true',
                        help='Discover what packages are imported by imports '
                              'in the script or modules being parsed. For '
                              'example, if the script you run makecite on '
                              'imports another package, and you want to cite '
                              'all packages used, use this flag.')

    parser.add_argument('--aas', action='store_true', dest='aas_tag',
                        default=False,
                        help='Also generate a AAS Latex \software{} tag with '
                             'all packages used.')

    parser.add_argument('paths', type=str, nargs='+',
                        help='A path, filename, or list of paths to search '
                             'for imported packages.')

    parser.add_argument('--version', action='version',
                        version=__version__)

    args = parser.parse_args(args)

    if not args.extensions:
        args.extensions = ['.py', '.ipynb']

    packages = get_all_packages(paths=args.paths,
                                extensions=args.extensions,
                                include_imported_dependencies=args.recursive)

    all_bibtex = ""
    y_citation = []
    n_citation = []
    name_to_tags = dict()
    for package in sorted(list(packages)):
        try:
            bibtex = get_bibtex_from_package(package)
            if bibtex is None:
                bibtex = get_bibtex_from_citation_file(package)
            if bibtex is None:
                bibtex = get_bibtex(package)
            y_citation.append(package)
            name_to_tags[package] = cite_tag_pattr.findall(bibtex)
        except ValueError:
            # Package doesn't have a .bib file in this repo. For now, just alert
            # the user, but we might want to try a web query or something?
            n_citation.append(package)
            continue

        all_bibtex = "{0}\n{1}".format(all_bibtex, bibtex)

    # print out some information about the packages identified, and ones
    # that don't have citation information
    print("Packages detected with citation information:")
    print("\t{0}".format(", ".join(y_citation)))

    print("\nPackages with no citation information:")
    print("\t{0}".format(", ".join(n_citation)))

    if args.output_file:
        # save .bib output file
        print("\nBibtex file generated: {0}".format(args.output_file))

        with open(args.output_file, 'a') as f:
            f.write(all_bibtex)

    else:
        print("\nBibtex:")
        print(all_bibtex)

    if args.aas_tag:
        cites = []
        for name, tags in name_to_tags.items():
            cites.append('{0} \\citep{{{1}}}'.format(name, ', '.join(tags)))

        software = r'\software{{{0}}}'.format(', '.join(cites))

        print("\nSoftware tag for AAS journals:")
        print(software)
