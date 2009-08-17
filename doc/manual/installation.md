#Prerequisites

Moa is developed on Ubuntu \citep{ubuntu} and RHEL \citep{rhel} Linux
and is expected to operate without much problems on most modern Linux
distributions. Moa is depends on the following list of software. The
version numbers are an indication, not strict prerequisites. Other,
even older, versions might work.

* Gnu Make 3.81 \citep{Gnumake}

* Git 1.6 \citep{git}. To download the Moa software. Alternatively it
  is possible to download a tarball.

* Python 2.6 \citep{python}. Python 2.5 will not work, several
  supporting scripts use 2.6 specific functionality

* Biopython 1.49 \citep{biopython}. Only used by the blast warpper.

* Apache Couchdb 0.9.0 \citep{couchdb} (Only when using couchdb functionality)

* Couchdb-python \citep{couchpy}

Furthermore, the required bioinformatics analysis tools need to be
installed. All Moa templates that wrap an application expect that
application to be installed and present in the PATH.

#Getting the code

Moa is hosted at github:

    http://github.com/mfiers/Moa

Currently there are no formal releases so the only option is to
download the latest version of the software, this can be done using
git \citep{git}:

    git clone git://github.com/mfiers/Moa.git

It is also possible to download an (automatically generated) archive
of the trunk. Using Git, however, makes it very easy to stay in sync
with the latest bugfixes and is thus strongly recommended until there
are formal releases. An archive can be found here:

    http://github.com/mfiers/Moa/tarball/master

After downloading, and possibly unpacking, the source code must be
moved to a suitable location of your choice. For example `/opt/moa`.
The resulting tree should contain the following directories:
`/opt/moa/bin` and `/opt/moa/template`. Remember to set the file
attributes, depending on who is going to use the software.

#Configuration

Configuration of Moa is simple: The Moa `/bin/` directory must be
included in the PATH and a environment variable must be set pointing
to the Moa directory. The easiest way to do this is by adding the
following lines to your `.bashrc`:

    export PATH=/opt/moa/bin:$PATH
    export MOABASE=/opt/moa

and run `source .bashrc`.

..done..
