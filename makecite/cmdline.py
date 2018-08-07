import os
from .discover import find_all_files
from .parsers import parser_map

def thing(paths, output_file, extensions, aas_tag):
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


def main(args=None):
    """TODO..."""

    from argparse import ArgumentParser

    parser = ArgumentParser(description='TODO: docs')

    parser.add_argument('-e', '--ext', action='append', dest='extensions',
                        default=None,
                        help='Specify the file extensions to look for and '
                             'parse. Currently, only .py and .ipynb are '
                             'supported.')

    parser.add_argument('-o', '--output-file', dest='output_file',
                        default='software-refs.bib',
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

    if not args.extensions:
        args.extensions = ['.py', '.ipynb']

    packages = thing(**vars(args))
    print(packages)
