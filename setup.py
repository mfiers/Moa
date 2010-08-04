#!/usr/bin/env python

import os
from distutils.core import setup
from distutils.command.install import INSTALL_SCHEMES

# see:
# http://groups.google.com/group/comp.lang.python/browse_thread/thread/35ec7b2fed36eaec/2105ee4d9e8042cb
for scheme in INSTALL_SCHEMES.values():
    scheme['data'] = scheme['purelib']

with open('VERSION') as F:
    version = F.read().strip()

scripts  = [os.path.join('bin', x) for x in """
moa              moainit.sh     moa_bash_completion
fastaSplitter    fastaNfinder   fastaInfo        fastaExtract
fasta2gff        blastReport    blastInfo        blast2gff
""".split()]

data_files = []
template_data = []
for dirpath, dirnames, filenames in os.walk('.'):
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'): del dirnames[i]
    if '__init__.py' in filenames: continue
    print dirpath
    data_files.append([dirpath, [os.path.join(dirpath, f) for f in filenames]])

setup(name='moa',
      version=version,
      description='Moa - automating command line bioinformatics',
      author='Mark Fiers',
      author_email='mark.fiers@plantandfood.co.nz',
      url='http://mfiers.github.com/Moa/',
      packages=['moa', 'moa.plugin'],
      package_dir = {'': os.path.join('lib', 'python')},
      scripts = scripts,
      data_files = data_files,
      requires = [
          'Jinja2 (>2.0)',
          'biopython (>1.50)',
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
