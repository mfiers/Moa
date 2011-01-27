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
Yaco provides a 'dict' like object that can be saved to disk as a YAML
file. Yaco can be used to store program configuration and make the
configuration data easily accessible. Keys of a Yaco object can be
accessed both as regular dict keys (`a['key']`) or as attributes
(`a.key`). Lower level dictionaries are automatically converted to
Yaco objects allowing similar access (`a.key.subkey`). Lists are
(recursively) parsed and dictionaries in list are converted to Yaco
objects allowing access allong the lines of `a.key[3].subkey`."""

setup(name='Yaco',
      version='0.1.5',
      description=DESCRIPTION,
      author='Mark Fiers',
      author_email='mark.fiers42@gmail.com',
      url='http://mfiers.github.com/Moa/api/Yaco.html',
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
