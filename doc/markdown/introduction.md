
'' NOTE '' Both the software and the manual are still under heavy development.  

Moa is a piece of software build around GNU Make \citep{Gnumake} that
allows you to use Gnu Make run bioinformatics pipelines.

GNU Make is an excellent tool to automate the compilation of
software. Gnu make determines how a file is created, what it's
dependencies are, and what needs to be executed. Gnu Make uses so
called Makefiles to describe a project. A bioinformatics project is
often of the same form as compiling software.

Moa wraps a set of common bioinformatics tools as Makefiles. Features
of Moa are:

* A uniform interface; all Moa makefiles use a central library that
	provides a uniform, command line, interface to configuring and
	executing jobs.

* Interaction; templates are designed to interact with each other,
    hence make it easy to build pipelines from these buliding blocks.

* Parallel execution; Gnu make facillitates parallel execution of
    jobs.
 

Apart from a set of template Makefiles, the Moa contains several other

* moaBase; a central library describing a number of central routines used by
	all Makefiles

* The "moa" helper script; a frontend to using Moa.

* Additional helper scripts; several of the template files require
	helper scripts that are part of the moa package.

* Couchdb interface; Moa is able to store information on each job in a
	couchdb. See chapter XX.


## Example session
To really understand how easy it is to use Moa, a sample session:
 
    mkdir test
    cd test
    moa new lftp

