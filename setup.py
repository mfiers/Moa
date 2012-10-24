#!/usr/bin/env python
"""
Moa setup script
"""

from setuptools import setup

entry_points = {
    'console_scripts': [
        'moa = moa.cli.main:dispatch',
        'moaprompt = moa.cli.moaprompt:moaprompt',
        'moar = moa.cli.moar:moar',
    ]}

requires = [
    'Jinja2>2.0',
    'GitPython>0.3',
    'pyyaml>3',
    'ruffus>=2.2',
    'Yaco>=0.1.7',
    'fist>=0.1.5',
    'unittest2>=0.5',
    'lockfile>=0.9',
    'mdGraph>=0.1'
    'markdown'
]

with open('VERSION') as F:
    version = F.read().strip()

packages = [
    'moa',
    'moa.cli',
    'moa.backend',
    'moa.backend.ruff',
    'moa.plugin',
    'moa.plugin.job',
    'moa.plugin.job.smw',
    'moa.plugin.system',
    'moa.plugin.system.doc',
    'moa.template',
    'moa.template.provider',
]

#uncertain how to deal with this :/
#data_files = (
#    ('/etc', ['moa/data/etc/config']),
#    ('/etc/profile.d', ['moa/data/etc/profile.d/moa.sh']),
#    ('/etc/bash_completion.d', ['moa/data/etc/bash_completion.d/moa']),
#)

setup(name='moa',
      version=version,
      description='Moa - command-line workflows (in bioinformatics)',
      author='Mark Fiers',
      author_email='mark.fiers.42@gmail.com',
      url='http://mfiers.github.com/Moa/',
      entry_points=entry_points,
      packages=packages,
      include_package_data=True,
      # data_files=data_files,
      zip_safe=False,
      install_requires=requires,
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
