#!/usr/bin/env python
from setuptools import setup, find_packages
setup(
 name = 'CustomeLibrary',
 version = '0.0.2',
 description = 'CustomeLibrary for Robot Framework',
 long_description = 'CustomeLibrary for Robot Framework',
 author = 'caiys',
 author_email = 'caiys@asiainfo-net.com',
 url = 'https://github.com/',
 license = 'MIT Licence',
 keywords = 'CustomeLibrary for robotframework',
 platforms = 'any',
 python_requires = '>=3.7',
 install_requires = [],
 package_dir = {'': 'src'},
 packages = ['CustomeLibrary']
 )