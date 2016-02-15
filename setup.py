# -*- coding: utf-8 -*-

from setuptools import setup

# TODO Is this the best way of testing for version?
import sys
if not sys.version_info[0] == 3:
    sys.exit("Python 3 is not supported.")

setup(
    name='guardian_haiku',
    version='1.0',
    packages=[
        'guardian_haiku'
    ],
    install_requires=[
        'lxml',
        'requests',
        'unidecode',
        'nltk'
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ]
)
