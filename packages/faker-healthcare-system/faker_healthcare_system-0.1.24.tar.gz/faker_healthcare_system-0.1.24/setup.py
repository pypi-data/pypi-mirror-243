#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function

from setuptools import setup, find_packages
from glob import glob
from os.path import splitext, basename, abspath, dirname, join

here = abspath(dirname(__file__))
try:
    README = open(join(here, "README.md")).read()
except:
    README = "An add-on provider for the Python Faker module to generate random and/or fake data."

CLASSIFIERS = [
    # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: Unix",
    "Operating System :: POSIX",
    "Operating System :: Microsoft :: Windows",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Topic :: Utilities",
]

setup(
    name="faker_healthcare_system",
    version="0.1.24",
    license="MIT",
    description="Health system related data provider for Faker module",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Maikel Aparicio",
    author_email="maikel.aparicio@theksquaregroup.com",
    url="https://github.com/MaikelAparicio10/faker_healthcare_system",
    packages=find_packages("faker_healthcare_system"),
    package_dir={"": "faker_healthcare_system"},
    package_data={"": ["*.csv"]},
    data_files=[("assets", ["assets/nucc_taxonomy_231.csv"])],
    py_modules=[
        splitext(basename(path))[0] for path in glob("faker_healthcare_system/*.py")
    ],
    include_package_data=True,
    zip_safe=False,
    classifiers=CLASSIFIERS,
    project_urls={
        "Source Code": "https://github.com/MaikelAparicio10/faker_healthcare_system",
        "Bug Reports": "https://github.com/MaikelAparicio10/faker_healthcare_system/issues",
        "Say Thanks!": "https://github.com/MaikelAparicio10/faker_healthcare_system",
    },
    python_requires=">=3.6",
    install_requires=["Faker>=19.13.0"],
    # test_requires=['pytest>=6.2', 'pytest-cov>=2.12.0'],
)
