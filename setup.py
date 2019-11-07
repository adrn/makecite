#!/usr/bin/env python

"""Setup script for the makecite package """

from setuptools import setup
from makecite import __version__

# Add entry point for `makecite` to be run as a script:
entry_points = {}
entry_points['console_scripts'] = ['makecite = makecite.cmdline:main']

with open('README.md') as f:
    LONG_DESCRIPTION = f.read()

setup(name='makecite',
      packages=['makecite'],
      version=__version__,
      setup_requires=[],
      tests_require=[],
      package_data={'makecite': ['makecite/bibfiles/*.bib']},
      include_package_data=True,
      description='Autogenerate bibtex citations for common Python packages',
      long_description=LONG_DESCRIPTION,
      long_description_content_type='text/markdown',
      author=('Adrian Price-Whelan, '
              'Alexandar Mechev, '
              'Julia Melo Rodrigues de Aguiar, '
              'Brigitta Sipocz, '
              'Leon Trapman'),
      author_email='adrn@astro.princeton.edu',
      url='https://github.com/adrn/makecite',
      download_url='https://github.com/adrn/makecite/archive/v0.0.1.tar.gz',
      keywords=['LaTeX', 'Astronomy', 'Citation', 'package management'],
      classifiers=['Development Status :: 1 - Planning',
                   'Intended Audience :: Developers',
                   'Intended Audience :: Science/Research',
                   "License :: OSI Approved :: MIT License",
                   "Natural Language :: English",
                   "Topic :: Scientific/Engineering :: Astronomy",
                   "Topic :: Text Processing :: Markup :: LaTeX",
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.4',
                   'Programming Language :: Python :: 3.5',
                   'Programming Language :: Python :: 3.6'
                   ],
      entry_points=entry_points, install_requires=['cffconvert']
      )
