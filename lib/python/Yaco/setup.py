#!/usr/bin/env python

import os
from distutils.core import setup
from distutils.command.install import INSTALL_SCHEMES

# see:
# http://groups.google.com/group/comp.lang.python/browse_thread/\
#      thread/35ec7b2fed36eaec/2105ee4d9e8042cb
for scheme in INSTALL_SCHEMES.values():
    scheme['data'] = scheme['purelib']

DESCRIPTION = """
Yaco - A dict like object that saves to and loads from yaml files.

Yaco is useful to store file configurations and make them easily
accessible. Yaco items can be accessed both as regular dict keys
(`a['key']`) or as attributes: (`a.key`).

"""

setup(name='Yaco',
      version='0.1',
      description=DESCRIPTION,
      author='Mark Fiers',
      author_email='mark.fiers42@gmail.com',
      url='http://mfiers.github.com/Moa/',
      packages=['Yaco', ],
      package_dir = {'Yaco': '.'},
      requires = [
          'PyYAML (>3.0)',
          ],
      classifiers = [
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.6',
          ]
     )
