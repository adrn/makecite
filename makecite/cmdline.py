# Standard library
import os
import re

# Package
from .discover import find_all_files
from .parsers import parser_map

_bib_path = os.path.join(os.path.split(os.path.abspath(__file__))[0],
                         'bibfiles')

def get_all_packages(paths, extensions=['.py', '.ipynb']):
    """Get a unique list (set) of all package names imported by all files of
    the requested extensions

    Parameters
    ----------
    paths : list, str
    extensions : list, iterable

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
    full_path = os.path.join(_bib_path, '{0}.bib'.format(package_name))
    if not os.path.exists(full_path):
        raise ValueError('Bibtex not found for {0}! If you know it has a '
                         'citation, please consider adding it via pull request '
                         ' to: https://github.com/adrn/makecite')

    with open(full_path, 'r') as f:
        bibtex = f.read()

    return bibtex

def main(args=None):
    from argparse import ArgumentParser

    parser = ArgumentParser(description='TODO: docs')

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

    parser.add_argument('--aas', action='store_true', dest='aas_tag',
                        default=False,
                        help='Also generate a AAS Latex \software{} tag with '
                             'all packages used.')

    parser.add_argument('paths', type=str, nargs='+',
                        help='A path, filename, or list of paths to search '
                             'for imported packages.')

    args = parser.parse_args(args)

    cite_tag_pattr = re.compile('@[a-zA-Z]+\{(.*),')

    if not args.extensions:
        args.extensions = ['.py', '.ipynb']

    packages = get_all_packages(paths=args.paths,
                                extensions=args.extensions)

    all_bibtex = ""
    y_citation = []
    n_citation = []
    name_to_tags = dict()
    for package in sorted(list(packages)):
        try:
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
        print("\nBibtex file generate: {0}".format(args.output_file))

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
