import os
from setuptools import setup, find_packages
from distutils.dir_util import copy_tree

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    install_requires = f.read().strip().split('\n')

setup(
    name="oscur",
    version="0.1",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://oscur.org',
    packages=['oscur'],
    package_dir = {
        'oscur': './src'
    },
    include_package_data=False,
    license_files = ('LICENSE'),
    python_requires='>=3.9',
    install_requires=install_requires
)
