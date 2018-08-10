# makecite
[![alt text](http://apmechev.com/img/git_repos/pylint/makecite.svg "pylint score")](https://github.com/apmechev/pylint-badge)
[![Build Status](https://travis-ci.org/adrn/makecite.svg?branch=master)](https://travis-ci.org/adrn/makecite)
[![Coverage Status](https://coveralls.io/repos/github/adrn/makecite/badge.svg?branch=master)](https://coveralls.io/github/adrn/makecite?branch=master)
[![License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat)](https://github.com/adrn/makecite/blob/master/LICENSE)
![badge-img](https://img.shields.io/badge/Made%20at-%23AstroHackWeek-8063d5.svg?style=flat)
[![DOI](https://zenodo.org/badge/143292502.svg)](https://zenodo.org/badge/latestdoi/143292502)


Generate latex + bibtex citation commands by looking at what packages are imported in your Python code.


## Installation

The recommended installation procedure is to use `pip`:

```
pip install makecite
```

To install the development version, you can `pip` install directly from this
GitHub repository with:

```
pip install git+https://github.com/adrn/makecite
```


## Examples

Get bibtex records for packages used in a single script, and store to a `.bib` file in the current working directory:

```
makecite my_script.py
```

Get bibtex records for packages used in all `.py` scripts in the current directory and store to a `.bib` file called "software_refs.bib":

```
makecite --ext=.py -o software_refs.bib .
```

Get bibtex records for packages used in all `.py` scripts and IPython notebook, `.ipynb`, files in two paths `my_code` and `my_notebooks`:

```
makecite --ext=.py --ext=.ipynb my_code my_notebooks
```

Get bibtex records for packages used in all `.py` scripts in the current directory and output a AAS journals `\software{}` tag:

```
makecite --ext=.py --aas .
```

## Citing this script

If you use this script, please consider citing [our Zenodo
record](https://zenodo.org/badge/latestdoi/143292502):

```
@misc{makecite:2018,
  author       = {Adrian Price-Whelan and
                  Alexandar Mechev and
                  jumeroag},
  title        = {adrn/makecite: v0.1},
  month        = aug,
  year         = 2018,
  doi          = {10.5281/zenodo.1343295},
  url          = {https://doi.org/10.5281/zenodo.1343295}
}
```


## License

Copyright 2018 the developers.

`makecite` is free software made available under the MIT License. For details
see the [LICENSE](https://github.com/adrn/makecite/blob/master/LICENSE) file.
