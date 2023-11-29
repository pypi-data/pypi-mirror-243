#!/usr/bin/env python
"""Script to install nijtaio."""
from distutils.core import setup
import io
import os

version = {}
with io.open(os.path.join('nijtaio', '_version.py')) as fp:
    exec(fp.read(), version)

setup(
    name='nijtaio',
    version=version['__version__'],
    packages=['nijtaio'],
    install_requires=['requests', 'soundfile', 'librosa', 'datasets', 's3fs'],
    entry_points={
        "console_scripts": ["voiceharbor = nijtaio.cli:main"],
    },
)
