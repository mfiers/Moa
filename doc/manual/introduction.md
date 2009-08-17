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

* Interaction; all templates are designed to interact with each other.

* Parallel execution; Gnu make bla bla bla
 
Moa consists of several parts:

* moaBase; a central library describing a number of central routines used by
	all Makefiles

* Template Makefiles; each application is wrapped in a template Makefile.

* The "moa" helper script; a number of tools that cannot be caught in
	Makefiles are implemented in a cental helper script called "moa".

* Additional helper scripts; a number of diverse utilities are part of
	the moa packages. These are a part of an embedded application.

* Couchdb interface; Moa is able to store information on each job in a
	couchdb. See chapter XX.


## Example session
To better understand how Moa works, please read this sample session:
 
    mkdir test
    cd test
    moa new lftp

