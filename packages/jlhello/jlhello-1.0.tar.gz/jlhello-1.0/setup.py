from setuptools import setup, find_packages
import codecs
import os

VERSION = '1.0'
DESCRIPTION = 'First package of Jalon L'
LOG_DESCRIPTION = 'A package that lets you print a simple hello greeting and byebye'

# Setting up
setup(
    name='jlhello',
    version=VERSION,
    description=DESCRIPTION,
    author='Jalon Liang',
    author_email='jalonliang@hello.com',
    packages=find_packages(),
    install_requires=['nothing'],
    keywords=['newbies', 'python', 'package', 'distribution'])
    	
