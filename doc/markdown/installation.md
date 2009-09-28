# Prerequisites

Moa is developed on Ubuntu \citep{ubuntu} and RHEL \citep{rhel} Linux
and is expected to operate without much problems on most modern Linux
distributions. Moa is depends on the following list of software. The
version numbers are an indication, not strict prerequisites. Other,
even older, versions might work.

* [Gnu Make](http://www.gnu.org/software/make/) 3.81

* [Git](http://git-scm.com/) 1.6. To download the Moa
  software. Alternatively it is possible to download a tarball.

* [Python](http://python.org) 2.6. Python version 2.5 and lower will
  not work, several supporting scripts use 2.6 specific functionality

* [Bash](http://www.gnu.org/software/bash/). Many of the embedded
  scripts expect the Bash shell. Luckily, Bash is the default shell of
  almost all Linux distributions.

* [Gnu Make Standard Library](http://sourceforge.net/gsml) (GSML). A
  set of standard routines for Gnu Make. GSML is embedded in this
  distribution.

## Couchdb

Moa can use Apache's Couchdb as a central storage of information on
Moa jobs. allowing other Moa jobs to refer hereto. If you want to use
this, the following prerequisites are added to the list:
 
* [Apache Couchdb](http://couchdb.apache.org/) 0.9.0. Only when using
  couchdb functionality, see the chapter on Couchdb

* [Couchdb-python](http://code.google.com/p/couchdb-python/). Only
  when using couchdb functionality, see the chapter on Couchdb

For more information, read the chapter on couchdb.

## Bioinformatics tools

Each of the wrapped tools, obviously, requires that these tools are
present. Usually, unless mentioned otherwise, Moa expects all tools to
be installed in the system PATH.  All requirements are described
in the reference chapter.

## Deciding where to install Moa

You will need to choose a location to install Moa to, this usually
depends on who is going to use the software. Moa can be installed
system wide for all users of this machine, for example in
`/opt/moa`. However, if you will be the only person using Moa, install
it in your home directory, for example under `~/moa`. The remainder of
this chapter assumes an installation in your home directory.

# Downloading Moa

Moa is hosted at github:

    http://github.com/mfiers/Moa

Currently there are no stable releases so the best option is to
download the latest version of the software, this can be done using
[Git](http://git-scm.com/) or by downloading a source archive.

## Using Git

Using git is a good choice as long as there are no releases. Git makes
it very easy to stay up to date with the latest version and, even
better, allows anybody to submit bugfixes to the Moa repository (more
on that later). To download Moa using Git, enter the following
commands (assuming you're installing Moa in your home directory):

    cd ~
    git clone git://github.com/mfiers/Moa.git moa


## Downloading an archive

As an alternative, it is possible to download an (automatically
generated) archive of the latest Moa version
[here](http://github.com/mfiers/Moa/tarball/master), for example,
using the following commands:
    
    wget http://github.com/mfiers/Moa/tarball/master


The archive that is downloaded will have a rather long name that looks
something like
`mfiers-Moa-b13ddf78c6a1ae9a714c7d9979a1b1de0ed08462.tar.gz`. This
archive needs to be unpacked in a temporary directory and then moved
to its final location:

    mkdir /tmp/moa_install
    cd /tmp/moa_install
    tar xvzf mfiers-Moa-b13ddf78c6a1ae9a714c7d9979a1b1de0ed08462.tar.gz
    mv mfiers-Moa-b13ddf78c6a1ae9a714c7d9979a1b1de0ed08462.tar.gz ~/moa




After following either procdure; downloading the archive or using Git,
the source code tree should be should be in its final location. The
tree should contain the following directories:

    ./moa
        ./bin
        ./doc
        ./etc
        ./lib
        ./template
        ./test
        ./util
        ./www
        ./COPYING
        ./INSTALL
        ./README
        ./VERSION

# Configuration

Configuration of Moa is simple: The Moa `/bin/` directory must be
included in the PATH and an environment variable must be set pointing
to the Moa directory. The easiest way to do this is by adding the
following lines to your `.bashrc`:

    export PATH=/opt/moa/bin:$PATH
    export MOABASE=/opt/moa

and run:

     source .bashrc

Also, if you are running Moa to be used by all users of your system
system, please remember the file attributes correctly:
    
    chmod a+rX -R $MOABASE
    chmod a+rx $MOABASE/bin/*

