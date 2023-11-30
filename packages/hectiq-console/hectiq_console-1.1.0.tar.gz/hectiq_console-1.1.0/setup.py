#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
__version__ = '1.1.0'

with open('README.md', encoding='utf-8') as f:
    readme = f.read()

requirements = [
    "requests",
    "toml",
    "pydantic"]

setup(
    name="hectiq_console",
    version=__version__,
    description="Python client to use the Hectiq Console",
    long_description=readme, 
    long_description_content_type='text/markdown',
    author="Edward Laurence",
    author_email="edwardl@hectiq.ai",
    url="https://console.hectiq.ai",
    packages=find_packages(),
    extras_require={
        "api": ["starlette"]
    },
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
    keywords='pip requirements imports',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering',
        'Intended Audience :: Science/Research',
    ]
)