#!/usr/bin/env python3

from setuptools import setup, find_packages

from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pmbootstrap_gtk',
    version='1.0a1',
    description='A GTK frontend for pmbootstrap',
    long_description=long_description,
    author='Martijn Braam',
    author_email='martijn@brixit.nl',
    install_requires=['pmbootstrap>=1.0'],
    url='https://www.postmarketos.org',
    license='GPLv3',
    python_requires='>=3.4',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='postmarketos pmbootstrap',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'pmbootstrap-gtk=pmbootstrap_gtk:main',
        ],
    },
)
