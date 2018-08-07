# makecite
[![alt text](http://apmechev.com/img/git_repos/pylint/makecite.svg "pylint score")](https://github.com/apmechev/pylint-badge)
[![Build Status](https://travis-ci.org/adrn/makecite.svg?branch=master)](https://travis-ci.org/adrn/makecite)
[![Coverage Status](https://coveralls.io/repos/github/adrn/makecite/badge.svg?branch=master)](https://coveralls.io/github/adrn/makecite?branch=master)
[![License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat)](https://github.com/adrn/makecite/blob/master/LICENSE)
![badge-img](https://img.shields.io/badge/Made%20at-%23AstroHackWeek-8063d5.svg?style=flat)

Generate latex + bibtex citation commands by looking at what packages are imported in your Python code.


## Examples

Get bibtex records for packages used in a single script, and store to a `.bib` file in the current working directory:

```
makecite my_script.py
```


Get bibtex records for packages used in all `.py` scripts in the current directory and store to a `.bib` file:

```
makecite --ext=.py .
```

Get bibtex records for packages used in all `.py` scripts and IPython notebook, `.ipynb`, files in two paths `my_code` and `my_notebooks`:

```
makecite --ext=.py --ext=.ipynb my_code my_notebooks
```


## Citing this script

TODO


## License

Copyright 2018 the developers.

`makecite` is free software made available under the MIT License. For details
see the [LICENSE](https://github.com/adrn/makecite/blob/master/LICENSE) file.
