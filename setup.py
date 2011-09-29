#!/usr/bin/env python

import os

from distutils.command.install import INSTALL_SCHEMES
from setuptools import setup

#for scheme in INSTALL_SCHEMES.values():
#    scheme['data'] = scheme['purelib']

with open('VERSION') as F:
    version = F.read().strip()

scripts  = [os.path.join('bin', x) for x in """
moa        fastaSplitter  fastaNfinder  fastaInfo  fastaExtract
fasta2gff  blastReport    blastInfo     blast2gff  moaprompt
moainit
""".split()]

data_files = []
template_data = []
exclude = ['build', 'sphinx', 'debian', 'dist', 'util', 'www']
for dirpath, dirnames, filenames in os.walk('.'):

    toRemove = []
    for dirname in dirnames:
        if dirname[0] == '.':
            toRemove.append(dirname)
            
        if dirpath == '.' and dirname in exclude:
            toRemove.append(dirname)

    for t in toRemove:
        dirnames.remove(t)

    if 'moa.egg-info' in dirpath: continue
    if dirpath[-5:] == '/dist': continue

    toRemove = []
    for filename in filenames:
        if filename[-1] in ['~']:
            toRemove.append(filename)
        if filename[0] in ['#', '.']:
            toRemove.append(filename)
    for t in toRemove:
        
        filenames.remove(t)

            
    if '__init__.py' in filenames: continue


    #np = os.path.join('./', dirpath)
    if dirpath[0] == '/':
        np = dirpath[1:]
    elif dirpath[:2] == './':
        np = dirpath[2:]
    else: np = dirpath
    data_files.append([np, [os.path.join(dirpath, f) for f in filenames]])

data_files.append(['etc/', ['./etc/config']])

setup(name='moa',
      version=version,
      description='Moa - lightweight bioinformatics pipelines',
      author='Mark Fiers',
      author_email='mark.fiers.42@gmail.com',
      url='http://mfiers.github.com/Moa/',
      packages=['moa',
                'moa.plugin',
                'moa.backend',
                'moa.backend.ruff',
                'moa.backend.gnumake',
                'moa.template',
                'moa.template.provider'
                ],
      package_dir = {'': os.path.join('lib', 'python')},
      scripts = scripts,
      data_files = data_files,
      install_requires = [
          'Jinja2>2.0',
          'GitPython>0.3',
          'pyyaml>3',
          'ruffus>=2.2',
          'Yaco>=0.1.7',
          'fist>=0.1.2',
          'unittest2>=0.5',
          'lockfile>=0.9',
          'mdGraph>=0.1'
          'markdown',
          ],
      classifiers = [
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: GNU General Public License (GPL)',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Unix Shell',
          'Topic :: Scientific/Engineering :: Bio-Informatics'
          ]
     )
