#-*- coding: utf-8 -*-

"""
    enpy
    ~~~~

    Setup
    `````
    $ pip install .
"""

from distutils.core import setup
import os

setup(
    name='enpy',
    version='0.0.1',
    url='http://github.com/mekarpeles/enpy',
    author='mek',
    author_email='michael.karpeles@gmail.com',
    packages=[
        'enpy',
        ],
    platforms='any',
    license='LICENSE',
    install_requires=[
    ],
    scripts=[
        "scripts/enpy"
        ],
    description="enpy is English syntax for Python",
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.md')).read(),
)
