Installation
============


Prerequisites
-------------

Moa is developed and tested on `Ubuntu <http://www.ubuntu.com>`_ and
`RHEL <http://www.redhat.com>`_ and is expected to operate without
much problems on most modern Linux distributions. You will need to
install the following prerequisites (and a large number more for each
of the templates). Version numbers are an indication, not strict
prerequisites. Other, even older, versions might work.


- `Python <http://python.org>`_ (2.6 or 2.7). Moa will not work with
  earlier versions, or with 3.0 and later.

- `Python-dev`: the Python development package. A few prerequisites
  installed by easy_install try to compile C libraries, and need
  this. Although all of them have backup, python only, alteratives;
  from a performace perspective it does probably not do any harm to
  have this installed::

    sudo apt-get install python-dev

- `python-yaml`:On ubuntu, this installs a fast YAML parser - using
  easy_install or pip might install a slower, python only, version::

    sudo apt-get install python-yaml

Git integration
...............

One feature of Moa is the ability to integrate with `Git
<http://git-scm.com/>`_ to keep track of your workflow. If you want to
use this, you (obviously) need Git installed. For most applications
the package manager version is fine. However, Moa is able to pull
templates from git repositories. If you want to use that feature,
you'll need to install `git subtree`. This application comes bundled
with recent version of Git (late 1.7 or 1.8), but needs to be
installed separately. Otherwise, it can be downloaded from the
`"apenwarr" <https://github.com/apenwarr/git-subtree>`_ repository.

Installation of Moa
-------------------

It is most convenient to install Moa from the
`Python package index <http://pypi.python.org/pypi/moa>`_::

    pip install Moa

Note that it is possible to install Moa within a `virtual env <http://pypi.python.org/pypi/virtualenv>`_. If you want to do this globally, you will need root rights.

Installation using git (from github)
-------------------------------------

When installing manuall, you'll need the following prerequisites:

- `pyyaml <http://pyyaml.org/wiki/PyYAML>`_
- `Jinja2 <http://jinja.pocoo.org/2/>`_
- `Ruffus <http://code.google.com/p/ruffus/>`_
- `gitpython <http://gitorious.org/git-python>`_
- `unittest2 http://pypi.python.org/pypi/unittest2`_
- `lockfile http://pypi.python.org/pypi/lockfile`_
- `GitPython http://pypi.python.org/pypi/GitPython`_

Once these are installed, you can get Moa from, `Github
<http://github.com/mfiers/Moa>`_. Make sure to clone the repository in
an appropriate location)::

    git clone git://github.com/mfiers/Moa.git moa

To install Moa, please run::

    cd moa
    python setup.py install

If this is for a global installation, you'll need to be root, or use sudo.

Moa should now work, try `moa --help`.

Troubleshooting
---------------

A potential problem is if your python version is NOT `python2.6` or
`python2.7` there are two options that you can pursue:

* Make sure python2.6 or 2.7 is installed.
* define an alias in your `~/.bashrc`: `alias moa='python2.7 moa'`
* create a symlink to python2.7 in your ~/bin directory and make sure
  that that is first in your path - but note that this will change
  your default Python to version 2.7

Bioinformatics tools
--------------------

Each of the wrapped tools requires the tools to be present. Usually,
Moa expects all tools to be present & executable on the system
PATH. The standard Moa distribution comes with wrappers for Blast, BWA
and Bowtie. Note that a number of tools also depends on `Biopython
<http://biopython.org/wiki/Main_Page>`_.

