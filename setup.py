#!/usr/bin/env python
"""
Setup script --
"""
import os
import glob

from setuptools import setup

with open('VERSION') as F:
    version = F.read().strip()

scripts = [os.path.join('bin', x) for x in """
moa        fastaSplitter  fastaNfinder  fastaInfo  fastaExtract
fasta2gff  blastReport    blastInfo     blast2gff  moaprompt
moainit    moar
""".split()]

data_files = []
template_data = []
exclude = ['build', 'sphinx', 'debian', 'dist', 'util', 'www']

data_files = [
    ('/usr/local/share/moa/template2', glob.glob('template2/*')),
    ('/usr/local/share/moa/logo', ['share/logo/moa.logo.txt']),
    ('/usr/local/share/moa/', ['VERSION', 'README', 'COPYING',
                               'Changelog.txt']),
    ('/usr/local/share/moa/test', glob.glob('share/test/*')),
    ('/etc/moa',  ['etc/config']),
    ('/etc/profile.d',  ['etc/profile.d/moa.sh']),
    ('/etc/bash_completion.d',  ['etc/bash_completion.d/moa']),
]

packagenames = []

for dirpath, dirnames, filenames in os.walk('./lib/python/moa'):

    toRemove = []
    for dirname in dirnames:
        if dirname[0] == '.':
            toRemove.append(dirname)

    for t in toRemove:
        dirnames.remove(t)

    pn = dirpath.replace('./lib/python/', '').replace('/', '.')
    packagenames.append(pn)

setup(name='moa',
      version=version,
      description='Moa - command-line workflows (in bioinformatics)',
      author='Mark Fiers',
      author_email='mark.fiers.42@gmail.com',
      url='http://mfiers.github.com/Moa/',
      packages=packagenames,
      package_dir={'': os.path.join('lib', 'python')},
      data_files=data_files,
      scripts=scripts,
      zip_safe=False,
      install_requires=[
          'Jinja2>2.0',
          'GitPython>0.3',
          'pyyaml>3',
          'ruffus>=2.2',
          'Yaco>=0.1.7',
          'fist>=0.1.5',
          'unittest2>=0.5',
          'lockfile>=0.9',
          'mdGraph>=0.1'
          'markdown',
      ],
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: GNU General Public License (GPL)',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Unix Shell',
          'Topic :: Scientific/Engineering :: Bio-Informatics'
      ])
