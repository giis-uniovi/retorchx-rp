# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='retorchCostCalculation',
    version='0.1.0',
    description='Sample package for Python-Guide.org',
    long_description=readme,
    author='Cristian Augusto',
    author_email='augustocristian@uniovi.esm',
    url='NONE',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
