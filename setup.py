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
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ]
)
