#!/usr/bin/env python
from setuptools import find_packages, setup

install_requires = [
    "Django>=2.0.1",
    "requests",
    "unidecode",
    "irsx @  https://github.com/datamade/990-xml-reader/releases/download/0.10/irsx-0.3.2-py3-none-any.whl",
]

setup(
    name="irsdb",
    version="0.0.1",
    author="Jacob Fenton",
    license="BSD",
    long_description="",
    url="",
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    platforms=["any"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
