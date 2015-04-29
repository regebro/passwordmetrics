#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import passwordmetrics

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='passwordmetrics',
    version=passwordmetrics.__version__,
    description='Checking the entropy of a password. Useful in password checkers.',
    long_description=readme + '\n\n' + history,
    author='Lennart Regebro',
    author_email='regebro@gmail.com',
    url='https://github.com/regebro/passwordmetrics',
    packages=[
        'passwordmetrics',
    ],
    package_dir={'passwordmetrics':
                 'passwordmetrics'},
    include_package_data=True,
    license="MIT",
    zip_safe=False,
    keywords='passwordmetrics',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    test_suite='tests',
)