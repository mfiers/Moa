# Prerequisites

Moa is developed and tested on [Ubuntu](http://www.ubuntu.com),
[RHEL](http://www.redhat.com) and
[Archlinux](http://www.archlinux.org) and is expected to operate
without much problems on all modern Linux distributions. Moa has the
following prerequisites (and a large number more for all templates).
The version numbers are an indication, not strict prerequisites.
Other, even older, versions might work.

* [Gnu Make](http://www.gnu.org/software/make/) (3.81)

* [Git](http://git-scm.com/) (1.6). Used to download the latest version,
  and possibly by the git plugin. 

* [Python](http://python.org) (2.6). Python version 2.5 and lower or
  3.0 will not work.

* [Bash](http://www.gnu.org/software/bash/) (4.1.2). Many of the
  embedded scripts expect the Bash shell. Luckily, Bash is the default
  shell of almost all Linux distributions.

* [Gnu Make Standard Library](http://sourceforge.net/gsml) (GSML). A
  set of standard routines for Gnu Make. GSML is distributed together
  with Moa.
 
* [Pandoc](http://johnmacfarlane.net/pandoc/) (Preferably 1.5). Pandoc
  is used in generating the on the fly help for which the ancient
  0.46, bundled with Ubuntu, will also work. Pandoc is also used to
  generating LaTeX & HTML documentation. For these a recent version is
  strongly recommended.

## Bioinformatics tools

Each of the wrapped tools, obviously, requires that these tools are
present. Usually, unless mentioned otherwise, Moa expects all tools to
be present on the system PATH.  Most templates check for prerequisite
tools to be present and will generate a clear error if this is not the
case.

# Installation from source

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

Currently there are no stable releases so the only option is to
download the latest version of the software using
[Git](http://git-scm.com/). Git makes it easy to stay up to date with
the latest version and, even better, allows anybody to submit code to
the Moa repository. To download Moa using Git (assuming installation
in `~/moa`)

    cd ~
    git clone git://github.com/mfiers/Moa.git moa


## Downloading a tarball

As an alternative, it is possible to download an (automatically
generated) archive of the latest Moa version from:
[http://github.com/mfiers/Moa/tarball/master](http://github.com/mfiers/Moa/tarball/master),
for example with the following command:
    
    wget http://github.com/mfiers/Moa/tarball/master


The archive that is downloaded will have a rather long name that looks
something like `mfiers-Moa-077a672.tar.gz`. This archive needs to be
unpacked in a temporary directory and then moved to its final
location:

    mkdir /tmp/moa_install
    cd /tmp/moa_install
    tar xvzf mfiers-Moa-077a672.tar.gz
    mv mfiers-Moa-077a672 ~/moa

After following either procdure you should have a directory with the
Moa source. It should, amongst others contain a `~/moa/bin` folder.

# Configuration

Configuration of Moa is simple: The Moa `/bin/` directory must be
included in the PATH and an environment variable must be set pointing
to the Moa directory. Moa has a script that does this for you:

    . ~/project/moa/bin/moainit.sh

(Note the dot!)

You can also add this line to your `~/.bashrc` and run `. ~/.bashrc`.

If you are installing Moa to be used by all users of your system
system, please remember to set the attributes:
    
    chmod a+rX -R $MOABASE
    chmod a+rx $MOABASE/bin/*

Moa should now work.
