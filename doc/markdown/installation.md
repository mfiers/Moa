# Ubuntu 10.04

If you are on an recent Ubuntu box - Moa can be installed from the
Launcpad PPA. Details on setting up the repository for your computer
can be found
[here](https://launchpad.net/~mfiers/+archive/moa-packages). After that, Moa, and all prerequisites can be installed using::

    apt-get install moa

# Other platforms

Moa is developed and tested on [Ubuntu](http://www.ubuntu.com) and
[RHEL](http://www.redhat.com) and is expected to operate without much
problems on all modern Linux distributions. Moa has the following
prerequisites (and a large number more for all templates).  The
version numbers are an indication, not strict prerequisites.  Other,
even older, versions might work.

* [Gnu Make](http://www.gnu.org/software/make/) (3.81)

* [Git](http://git-scm.com/) (1.6). Used to download the latest version,
  and optionally by the git plugin. 

* [Python](http://python.org) (2.6). Python version 2.5 and lower or
  3.0 will not work.

* [Bash](http://www.gnu.org/software/bash/) (4.1.2). Many of the
  embedded scripts expect the Bash shell. Luckily, Bash is the default
  shell of almost all Linux distributions.

* [Gnu Make Standard Library](http://sourceforge.net/gsml) (GSML). A
  set of standard routines for Gnu Make. GSML is distributed together
  with Moa.
 
* [Pandoc](http://johnmacfarlane.net/pandoc/) (Preferably 1.5) is used
  in generating help. Pandoc is also used to generating Pdf and HTML
  documentation. A recent version is recommended.

* [Jinja2](http://jinja.pocoo.org/2/) is used together with Pandoc to
  generate the documentation, website, pdf manual, man
  pages. If you have easy_install: `easy_install jinja2`.

## Bioinformatics tools

Each of the wrapped tools, obviously, requires that these tools are
present. Usually, unless mentioned otherwise, Moa expects all tools to
be present on the system PATH.  Most templates check for prerequisite
tools to be present and will generate a clear error if this is not the
case.

## Installation from source

## Deciding where to install Moa

You will need to choose a location to install Moa to, this usually
depends on who is going to use the software. Moa can be installed
system wide for all users of this machine, for example in
`/opt/moa`. However, if you will be the only person using Moa, install
it in your home directory, for example under `~/moa`. The remainder of
this chapter assume installation in the latter location.

## Downloading Moa

Moa is hosted at github:

    http://github.com/mfiers/Moa

You can either download the latest release from:

    http://github.com/mfiers/Moa/downloads

Or use Git [Git](http://git-scm.com/) to get the development
version. Git makes it easier to stay up to date with the latest
version, and currently there is not much difference between the releases and the development version. To download Moa using Git (assuming installation in
`~/moa`)

    cd ~
    git clone git://github.com/mfiers/Moa.git moa


To download the latest release as an archive us a command along the
folowing lines"
    
    wget http://github.com/mfiers/Moa/tarball/v0.9.3


The archive that is downloaded will have a rather long name that looks
something like `mfiers-Moa-v0.9.3-077a672.tar.gz`. This archive needs
to be unpacked in a temporary directory and then moved to its final
location:

    mkdir /tmp/moa_install
    tar xvzf mfiers-Moa-077a672.tar.gz -C /tmp/moa_install
    mkdir ~/moa
    mv /tmp/moa_install/mfiers-Moa-077a672 ~/moa

After following either procdure you should have a directory with the
Moa source. It should, amongst others contain a `~/moa/bin` folder.

# Configuration

Configuration of Moa is simple: The Moa `/bin/` directory must be
included in the PATH and an environment variable must be set pointing
to the Moa directory. Moa has a script that does this for you:

    . ~/moa/bin/moainit

(Note the dot!, alternatively use: `source ~/moa/bin/moainit`)

It is probably a good idea to add this line to your `~/.bashrc` for future sessions.

If you are installing Moa to be used by all users of your system
system, please remember to set the attributes:
    
    chmod a+rX -R $MOABASE
    chmod a+rx $MOABASE/bin/*

Moa should now work, try `moa help`
