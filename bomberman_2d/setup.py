"""
Module containing the setup for unit tests.

This module uses setuptools to define the configuration for packaging the 'src' package.

Attributes:
    name (str): The name of the package.
    packages (List[str]): List of packages to be included in the distribution.

Methods:
    setup: Configures the package using setuptools.
"""
from setuptools import setup, find_packages

setup(name="src", packages=find_packages())