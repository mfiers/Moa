
.. _install-label:

Installation
============


Prerequisites
-------------

Moa is developed and tested on `Ubuntu <http://www.ubuntu.com>`_ and
`RHEL <http://www.redhat.com>`_ and is expected to operate without
much problems on most modern Linux distributions. Moa requires `Python
<http://python.org>`_ (2.6 or 2.7). Moa will not work with earlier
versions or with Python3.

Recommended prerequisites are:

- `python-dev`: The Python development libraries. A number of
  prerequisites installed by pip or easy_install will try to compile C
  libraries, and need this. Although all have a backup, Python only,
  version - the performance of the C, performance will suffer. On a
  debian based distribution, call::

    sudo apt-get install python-dev

  While on RHEL flavoured distribution users might run::

    sudo yum install -y python-devel

- `python-yaml`: This will install a faster YAML parser, as opposed to
   the python only YAML parser you would probably get when installing
   through pip or easy-install. On a debian based distro::
   
    sudo apt-get install python-yaml
    
  While on RHEL flavoured distribution users will find this in the
  `EPEL <http://fedoraproject.org/wiki/EPEL>`_ repository and might
  want to run::
  
    sudo yum install -y pyyaml

Git integration
...............

One feature of Moa is the ability to integrate with `Git
<http://git-scm.com/>`_ to keep track of your workflow. If you want to
use this, you (obviously) need Git installed. For most applications
the package manager version is fine. However, Moa is able to pull
templates from git repositories. If you want to use that feature, you
must install `git subtree`. This application comes bundled with recent
version of Git (certainly with 1.8) but still needs to be installed
separately. Otherwise, it can be downloaded from the `"apenwarr"
<https://github.com/apenwarr/git-subtree>`_ repository.


Blue Ringed Octopus
-------------------

Blue Ringed Octopus is a (randomly named) repository with a number of
helper scripts, used by a number of templates. You might want to
install this - just check out the repository and either add it to your
PATH, or copy the scripts to a location in the PATH. The repository
can be found here::

    https://github.com/mfiers/Blue-Ringed-Octopus

Installation of Moa
-------------------

It is most convenient to install Moa from the
`Python package index <http://pypi.python.org/pypi/moa>`_::

    pip install Moa

(You might need root rights to do this, also - pip is similar to
easy_install, so if you want you can run `easy_install Moa`)

You will definitely need `pip <http://www.pip-installer.org>`_ installed
to run the pip command above which is a replacement for easy_install.

Note that it is possible, and even recommended, to install Moa within
a `virtual environment <http://pypi.python.org/pypi/virtualenv>`_.

Moa should now work, try `moa --help`.

Bash integration
................

Moa comes with a number of functions to improve integration with
Bash. To turn these on, execute the following command (or add this to
your `~/.bashrc`)::

    source $(moainit)

This does a number of things:

* adds an alias `msp` for `moa set process`
* adds tab completion
* records a bash history for each separate moa job, equivalent to your
  bash history, but stored with your job.

  **Note that this is a possible privacy concern**. Commands that are
  not related to your workflow will be recorded (and possibly shared)
  as well. If you want to remove your history, delete
  `.moa/local_bash_history`. For a complete workflow run (in the root
  of that workflow)::

       find . -name local_bash_history | xargs rm

  The local_bash_history is, however, not tracked by the Git module
  (unless specified explicitly)

Manual installation (from Github)
---------------------------------

When installing manually, you'll need the following prerequisites:

- `pyyaml <http://pyyaml.org/wiki/PyYAML>`_
- `argparse <http://pypi.python.org/pypi/argparse>`_ (only for Python2.6)
- `Jinja2 <http://jinja.pocoo.org/2/>`_
- `ruffus <http://code.google.com/p/ruffus/>`_
- `unittest2 <http://pypi.python.org/pypi/unittest2>`_
- `lockfile <http://pypi.python.org/pypi/lockfile>`_
- `GitPython <http://pypi.python.org/pypi/GitPython>`_
- `Yaco <http://pypi.python.org/pypi/Yaco>`_
- `fist <http://pypi.python.org/pypi/fist>`_

Once these are installed, you can get Moa from, `Github
<http://github.com/mfiers/Moa>`_. Run the following command (in an
appropriate location)::

    git clone git://github.com/mfiers/Moa.git

To install Moa, run::

    cd Moa
    python setup.py install

If this is for a global installation, you'll need to be root, or use sudo.

Moa should now work, try `moa --help`.

Troubleshooting
---------------

A potential problem could be that your python version is NOT
`python2.6` or `python2.7` there are a few options that you can pursue:

* Make sure python2.6 or 2.7 is installed.
* define an alias in your `~/.bashrc`: `alias moa='python2.7 moa'`
* create a symlink to python2.7 in your ~/bin directory and make sure
  that that is first in your path - but note that this will change
  the Python version for all you user scripts.

Bioinformatics tools
--------------------

Each of the wrapped tools requires the tools to be present. Usually,
Moa expects all tools to be present & executable on the system
PATH. The standard Moa distribution comes with wrappers for Blast, BWA
and Bowtie. Note that a number of tools also depends on `Biopython
<http://biopython.org/wiki/Main_Page>`_.

