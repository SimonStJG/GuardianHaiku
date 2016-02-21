# -*- coding: utf-8 -*-

from setuptools import setup

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
        'nltk',
        'typing'
    ],
    tests_require=[
        'pytest-runner',
        'pytest >= 2.8.7',
        'pytest-cov == 2.2.1'
    ]
)
