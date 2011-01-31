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
Fist / File sets

Handle & map sets of files. Fist allows the definition of sets of
files and deriving mapped sets. See
http://mfiers.github.com/Moa/api/fist.html for more information
""".strip()
 
setup(name='fist',
      version='0.1.1',
      description=DESCRIPTION,
      author='Mark Fiers',
      author_email='mark.fiers42@gmail.com',
      url='http://mfiers.github.com/Moa/',
      packages=['fist', ],
      package_dir = {'fist': '.'},
      requires = [],
      classifiers = [
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.6',
          ]
     )
