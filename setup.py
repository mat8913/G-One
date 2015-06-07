#!/usr/bin/env python3
from setuptools import setup, find_packages

setup(
    name="G - One",
    version="0.1",
    packages=find_packages(),
    entry_points={
        'gui_scripts': [
            'G-One = g.one.main:main',
        ]
    },
    package_data={
        'g.one.resources': ['*.png', '*.wav']
    }
)
