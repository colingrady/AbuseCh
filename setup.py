#!/usr/bin/env python

import os
from setuptools import setup, find_packages

from _version import __version__


# Read the install requirements list
with open(os.path.join(os.path.dirname(__file__), 'requirements.txt'), 'r') as fh:
    requirements = fh.read().strip().splitlines()


# Setup
setup(
    name='AbuseCh',
    version=__version__,
    description='Abuse.ch APIs Python Library',
    author='Colin Grady',
    author_email='cogrady@cisco.com',
    url='https://github.com/colingrady/AbuseCh',
    python_requires='>=3.6',
    packages=find_packages(include='AbuseCh.*'),
    install_requires=requirements
)
