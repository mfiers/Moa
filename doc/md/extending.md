This chapter describes how to create new templates for use with
Moa. Creating a template is not very difficult, once you have a basic
understanding of how Makefiles work. Pprobably the hardest part is
ensuring that templates are able to interact with other templates.

A template is, as stated, not much more than Makefile that adheres to
certain standards. To understand how Makefiles work, please read the
[Gnu Make
Manual](http://www.gnu.org/software/make/manual/make.html). Note that
creating Makefiles can be somewhat complex at first, given that the
logic differs from scripting languages. The easiest way to do this is
to work from an existing Makefile.

Each template exists of the following parts:

* Definition 
* Include moaBase
* Implementation

The order in which everything is defined in a template is very
important! It is advisable to not define variables depending on other
variables in the definition phase. 

In the remainder of this chapter we will describe a simple template
that creates the reverse complement of a
[FASTA](http://en.wikipedia.org/wiki/FASTA_format) file using the
[EMBOSS](http://emboss.sourceforge.net/)\citep{Ric00}
[revseq](http://emboss.sourceforge.net/apps/release/6.1/emboss/apps/revseq.html)
utility

# Definition

The definition is a list of variables defining what your template does
and giving Moa information on how to use this template.

## Describing the new template

The following variables define what your template does. These
variables are used in generating the help files, the manual and the
website.

Identifier           Description
-----------------    ---------------------------------------------------
moa_title            The title for this template
moa_description      A short description of this template
moa_ids              A unique, short, identifier for this template

Example:

     moa_title = Reverse Complement
     moa_description = This Moa template takes a set of      \
         input FASTA sequences and determines the reverse    \
         complement using the EMBOSS revseq utility.
     moa_ids += revcom

Note that lines are allowed to break over multiple lines, given that
each line that continues to the enxt line ends with a backslash. No
spaces are allowd after the backslash and the new line must be
indented (with at least one space).

## Moa organizational units - moa_ids

In the previous chapter, both title and description are fairly self
evident. The `moa_ids` variable is, however, more complicated. Each
template must have, at least one, unique, preferaby short, identifier
linked to it. This `moa_id` helps in defining variable space for each
template. The moa_id returns when defining template specific variables
and targets. All template specific variables have the moa\_id as a
part of their name, so do the major targets of a template.

Use of uniqued ids allow Moa to stack several templates into a larger,
more complicated, templates. This might be usefull describing a set of
resembling tasks that have a lot of overlapping code. Another powerful
use is to create complex jobs that execute a mini-pipeline in one
run. For example, gathering a filter a specific set of sequences
(using the gather template) and creating a BLAST database from that.

Using ids allows functional sepeartion of tasks withing a template, or
within a stacked template. It is advisable to start creating templates
with only one task. For each task, a set of specific variables need to
be defined.

Given that a template can define multiple tasks, a moa\_id are added
to the moa\_ids array using the following syntax:

    moa_ids += revcomp

## taks specfic variables


Identifier           Description
-----------------    ---------------------------------------------------
moa_title            The title for this template
moa_description      A short description of this template
moa_ids              A unique, short, identifier for this template


# Include moaBase

To includie moaBase add the following line to your Makefile:

    include $(shell echo $$MOABASE)/template/moaBase.mk

# Implementation

## define dependant variables

## define targets

Each task, identified by a unique moa\_id, needs to define a set of
four targets. For example, if your template defines: `moa_id +=
revomp` then the following four targets are expected to be defined and
are automatically executed:

* MOA\_ID - revcomp
* MOA\_ID\_prepare - revcomp_prepare
* MOA\_ID\_post - revcomp_post
* MOA\_ID\_clean - revcomp_clean

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

 
