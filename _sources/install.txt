Installation
============


Prerequisites
-------------

Moa is developed and tested on `Ubuntu <http://www.ubuntu.com>`_ and
`RHEL <http://www.redhat.com>`_ and is expected to operate without
much problems on all modern Linux distributions. Moa has the following
prerequisites (and a large number more for all templates). Version
numbers are an indication, not strict prerequisites. Other, even
older, versions might work. 


- `Python <http://python.org>`_ (2.6 or 2.7). Moa will not work with
  versions earlier, or with 3.0 and up

- `Git <http://git-scm.com/>`_ (1.6). Necessary either to download the
  Moa software from github, or, to make use of the integrated version
  control.

- A number of support scripts & templates depend on `Biopython
  <http://biopython.org/wiki/Main_Page>`_. Consider installing it
  before starting to use Moa.

- `Python-dev`: the Python development package. A few prerequisites
  installed by easy_install try to compile C libraries, and need
  this. Although all of them have backup, python only, alteratives;
  from a performace perspective it is probably smart to have this
  installed::

    sudo apt-get install python-dev

- `python-yaml`:On ubuntu, this installs a fast YAML parser - using
  easy_install or pip might install a slower, python only, version::

    sudo apt-get install python-yaml

Python prerequisites
--------------------

These prereqs can be installed manually or with `easy_install` or
`pip`:

- `pyyaml <http://pyyaml.org/wiki/PyYAML>`_ (unless already installed)
- `Jinja2 <http://jinja.pocoo.org/2/>`_ 
- `Ruffus <http://code.google.com/p/ruffus/>`_
- `gitpython <http://gitorious.org/git-python>`_
- `unittest2 http://pypi.python.org/pypi/unittest2`_
- `lockfile http://pypi.python.org/pypi/lockfile`_


Not part of the list of prerequisites are the following libraries, which
you'll only need if you are planning to run the web interface:

- `ElementTree <http://effbot.org/zone/element-index.htm>`_
- `Markdown <http://freewisdom.org/projects/python-markdown/>`_


Bioinformatics tools
--------------------

Each of the wrapped tools requires the tools to be present. Usually,
Moa expects all tools to be present & executable on the system
PATH. The standard Moa distribution comes with wrappers for:

- Blast
- BWA
- Bowtie
- Soap

and many more


Installing git (from github)
----------------------------

Moa is hosted on, and can be installed from, `github <http://github.com/mfiers/Moa>`_::

    cd ~
    git clone git://github.com/mfiers/Moa.git moa

Note - their is also a copy of moa in the python package index - this
one is almost certainly outdated, and is currently not supported.

Configuration
-------------

Configuration of Moa is simple, and can be done by sourcing the
`moainit` script::

    . ~/moa/bin/moainit

(Note the dot!, alternatively use: ``source ~/moa/bin/moainit``)

It is probably a good idea to add this line to your ``~/.bashrc`` for
future sessions.

Moa should now work, try `moa --help`.

If your default python version is NOT `python2.6` or `python2.7` there
are a few options that you can pursue:

* change the hashbang of the `moa` script
* define an alias in your `~/.bashrc`: `alias moa='python2.6 moa'`
* create a symlink to python2.6 in your ~/bin directory and make sure
  that that is first in your path.

Installing the web interface
----------------------------

Note - this is highly experimental - you will probably need to fiddle
with the configuration files to get it working. Start with installing
apache2.

Then - assuming that:
* Your Moa work directory is under /home/moa/work
* Your Moa is installed in /opt/moa Create a file in
`/etc/apache2/conf.d/moa.conf` with the following approximate
contents::

    Alias /moa/data /home/moa/work
    <Directory /home/moa/work>
       Options +Indexes +FollowSymLinks
       Order allow,deny
       Allow from all

       SetEnv MOADATAROOT /home/moa/work
       SetEnv MOAWEBROOT /moa/data

       IndexOptions FoldersFirst SuppressRules HTMLTable IconHeight=24 SuppressHTMLPreamble SuppressColumnSorting SuppressDescription

       HeaderName /moa/cgi/indexHeader.cgi
       ReadmeName /moa/html/indexFooter.html
    </Directory>

    ScriptAlias /moa/cgi/ /opt/moa/www/cgi/
    <Directory /opt/moa/www/cgi/>
        AddType text/html .cgi
        Order allow,deny
        Allow from all
        SetEnv MOABASE /opt/moa
    </Directory>

    Alias /moa/html/ /opt/moa/www/html/
    <Directory /opt/moa/www/html>
        Order allow,deny
        Allow from all
        Options +Indexes
    </Directory>

You might want to check the #! of `/opt/moa/www/cgi/indexHeader.cgi`
depending on your system configuration. Restart apache and it should
work
