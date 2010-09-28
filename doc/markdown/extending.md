# extending Moa

Note: this is a work in progress - and currently not finished

This chapter describes how to create new templates for use with
Moa. Creating a basic template is not difficult, once you have a basic
understanding of how Makefiles work. Probably the hardest part is
ensuring that templates are able to interact with other templates.


## Creating a simple template - example
A template is, as stated, basically a Makefile that adheres to a set
of standards. To understand how Makefiles work, please read the [Gnu
Make Manual](http://www.gnu.org/software/make/manual/make.html). Note
that creating Makefiles can be somewhat complex at first, given that
the logic differs from scripting languages. The easiest way to do this
is to work from an existing Makefile.

Each template exists of two parts:

* Definitions
* Implementation

This order is very important! Parts of the Moa core are included
inbetween the definitions and the implementation. Getting the order
wrong might cripple your template.

In the remainder of this chapter we will describe how to implement a
new tool base on a simple example that creates the reverse complement
of a [FASTA](http://en.wikipedia.org/wiki/FASTA_format) sequence using
the [EMBOSS](http://emboss.sourceforge.net/)\citep{Ric00}
[revseq](http://emboss.sourceforge.net/apps/release/6.1/emboss/apps/revseq.html)
utility.

All templates are stored in the `$MOABASE/template` directory. This
template will be stored under the name `revseq.mk`.

## Definitions

Each template start with including the first part of the Moa core:

    include $(MOABASE)/template/moa/prepare.mk

`moaBasePre` defines a set of default Moa variables and has some
macro's that make variable definition easier. The template defintion
continues by defining a set of variables used in the latter part of
the template.

## Describing the new template

The following variables define what your template does. These
variables are used in generating the help files, the manual and the
website.

Identifier           Description
-----------------    ---------------------------------------------------
moa_title            A short title for this template
moa_description      A short description of this template

For our Revseq example:

     moa_title = Revseq
     moa_description = This Moa template takes a set of      \
       input FASTA sequences and determines the reverse      \
       complement using the EMBOSS revseq utility.
     moa_ids += revcom

Note that lines are allowed to break over multiple lines, given that
each line that continues to the next line ends with a backslash. No
spaces are allowd after the backslash. Indenting the next line is not
necessary, but it does enhance readability.

### namespace definition: `moa_ids`

Each MOA template defines a set of variables and targets (things to
do). These variables and targets (usually) share a single id in their
name. In the case of template variables this is a convention, making
templates easier to read. Targets, however, are often executed
automatically, based on the expected name. A `moa_id` is defined in
the following way (for our example):

    moa_ids += revseq

A `moa_id` should be unique and is ideally short and consise. It is
also advisable to save the template under the same name.
    

### job specific variables

The next part of the definitions can be used freely to define
variables to be used in the implementation. Each of these variables,
ideally, start with the `moa_id` (but this is not enforced). The
advantage of defining variables here is that they will be accessible
via the command line and the API. For example, you can set a define
variable using the following command line:

    moa set title='Descriptive title'    


There are two types of variables that can be defined: mandatory and
optional.

Identifier           Description
-----------------    ---------------------------------------------------
moa\_title            The title for this template
moa\_description      A short description of this template
moa\_ids              A unique, short, identifier for this template


Most templates will have variables specific to the job. These can be defined by  

### optional job specific variables

## Include the moa core library

To include the core moa library, the following line needs to be added to the Makefile

    include $(shell echo $$MOABASE)/template/moa.core.mk

## Implementation

## define targets

Each task, identified by a unique moa\_id, needs to define a set of
four targets. For example, if your template defines: `moa_id +=
revomp` then the following four targets are expected to be defined and
are automatically executed:

* $(moa_id): revcomp
* $(moa_id)_prepare: revcomp_prepare
* $(moa_id)_post - revcomp_post
* $(moa_id)_clean - revcomp_clean

Each of these targets must be defined in a new template, although they
could can be empty. In the following paragraphs, each of these targets
are discussed, in the order that they are executed.

### Prepare execution: revcomp_prep

The MOA\_ID\_prep target contains commands that are executed prior to
the main run. In the case of reverse complementing sequences this
target can be used to create a directory to store the output
sequences. Using a separate subdirectory to 

### Round up execution: revcomp_post

### Clean up: revcomp_clean


* **revcomp**: the main target, executes the main task of this
    template. In this case it takes a set of input sequences and write
    the reverse complement back to disk.

* **revcomp_prepare**: 

* **revcomp_post**: Optional commands to be exeucted after everything
    is finished. In the case of reverse complementing a set of
    sequences there is not much to do. The BLAST template, however,
    uses this target to create an overall BLAST report

* **revcomp_clean**: Cleans up all reverse complemented sequences

