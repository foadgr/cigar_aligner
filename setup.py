#!/usr/bin/env python
# -*- coding: utf-8 -*-


import io
import os
import sys
import csv
from shutil import rmtree

from setuptools import find_packages, setup
from distutils.cmd import Command
from setuptools.command.build_py import build_py

# Package meta-data.
NAME = 'cigar_task'
DESCRIPTION = 'Cigar functionality task'
URL = 'https://github.com/foadgr/cigar_task'
EMAIL = 'foadgreen@gmail.com'
AUTHOR = 'Foad Green'
REQUIRES_PYTHON = '>=3.7.0'
VERSION = '0.1'

# Required packages
REQUIRED = [
    'pandas', 'csv', 're'
]


EXTRAS = {}


here = os.path.abspath(os.path.dirname(__file__))

try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the package's __version__.py module as a dict.
about = {}
if not VERSION:
    project_slug = NAME.lower().replace("-", "_").replace(" ", "_")
    with open(os.path.join(here, project_slug, '__version__.py')) as f:
        exec(f.read(), about)
else:
    about['__version__'] = VERSION


class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = [
        ('only_required=', None, 'Only create required data.'),
        ('all_tests=', None, 'Crate all test data.')
    ]

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        """Set default values for options."""
        pass

    def finalize_options(self):
        """Post-process options."""
        pass

    def run(self):
        """Run command"""
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPI via Twine…')
        os.system('twine upload dist/*')

        self.status('Pushing git tags…')
        os.system('git tag v{0}'.format(about['__version__']))
        os.system('git push --tags')
        
        sys.exit()


class CreateData(Command):
    """A custom setup command to create test data files"""

    description = 'Create test data files'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        """Set default values for options."""
        pass

    def finalize_options(self):
        """Post-process options."""
        pass

    def run(self):
        """Run command."""
        self.status('Creating data tables')

        # Generate data tables for main specification
        req_dir = os.path.join(here, 'cigar_task/data/main_spec')
        os.system(f'mkdir -p {req_dir}')
        with open(os.path.join(req_dir,'input_01.tsv'), 'w') as f:
            writer = csv.writer(f, delimiter='\t', quotechar='"')
            writer.writerow(['TR1', 'CHR1', '3', '8M7D6M2I2M11D7M'])
            writer.writerow(['TR2', 'CHR2', '10', '20M'])
        with open(os.path.join(req_dir,'input_02.tsv'), 'w') as f:
            writer = csv.writer(f, delimiter='\t', quotechar='"')
            writer.writerow(['TR1', '4'])
            writer.writerow(['TR2', '0'])
            writer.writerow(['TR1', '13'])
            writer.writerow(['TR2', '10'])
        self.status(f'Data tables created in path: {req_dir}')

        # Generate test data tables
        test_dir = os.path.join(here, 'cigar_task/data/tests')
        os.system(f'mkdir -p {test_dir}')
        with open(os.path.join(test_dir,'input_01.tsv'), 'w') as f:
            writer = csv.writer(f, delimiter='\t', quotechar='"')
            writer.writerow(['TR1', 'CHR1', '3', '8M7D6M2I2M11D7M'])
            writer.writerow(['TR2', 'CHR2', '10', '20M'])
        with open(os.path.join(test_dir,'input_02.tsv'), 'w') as f:
            writer = csv.writer(f, delimiter='\t', quotechar='"')
            writer.writerow(['TR1', '4'])
            writer.writerow(['TR2', '0'])
            writer.writerow(['TR1', '13'])
            writer.writerow(['TR2', '10'])
        self.status(f'Data tables created in path: {test_dir}')

        sys.exit()

# Setup the build:
setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=long_description,
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=('tests',)),
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
    cmdclass={
        'upload': UploadCommand,
        'create_data': CreateData
    },
)