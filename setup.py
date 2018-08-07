#!/usr/bin/env python
"""Setup script for the makecite package
"""
#from distutils.core import setup
from setuptools import setup
import makecite

setup(name='makecite',
      packages=[],
      version=makecite.__version__,
      setup_requires=[],
      tests_require=[],
      include_package_data=True,
      description='Package for making bibtex citation strings for common python packages',
      long_description="Searching through a folder's python and python Notebook "
      "files and creates a bibtex string for all used packages",
      author='Adrian Price-Whelan, Alexandar Mechev, Julia Melo Rodrigues de Aguiar',
      author_email='LOFAR@apmechev.com',
      url='https://www.github.com/adrn/makecite',
      download_url='https://github.com/adrn/makecite/archive/v0.0.1.tar.gz',
      keywords=['LaTeX','Astronomy','Citation','package management'],
      classifiers=['Development Status :: 1 - Planning',
                   'Intended Audience :: Developers',
                   'Intended Audience :: Science/Research',
                   "License :: OSI Approved :: MIT License",
                   "Natural Language :: English",
                   "Topic :: Scientific/Engineering :: Astronomy",
                   'Programming Language :: Python :: 2.6',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.2',
                   'Programming Language :: Python :: 3.3',
                   'Programming Language :: Python :: 3.4',
                   'Programming Language :: Python :: 3.5',
                   'Programming Language :: Python :: 3.6'
                   ]
     )

