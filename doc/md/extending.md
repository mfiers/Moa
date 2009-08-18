This chapter describes how to create new templates for use with
Moa. Creating a template is not extremely difficult, probably the
hardest part is ensuring that templates are able to interact with
other templates.

A template is nothing more than a standardized Makefile. To understand
how Makefiles work, please read the [Gnu Make
Manual](http://www.gnu.org/software/make/manual/make.html). Note that
creating Makefiles can be difficult at first, as the logic rather
differs from scripting languages.

Each template exists of the following parts:

* Definition 
* Include moaBase
* Implementation

The order in which the template is defined is very important! 

In the remainder of this chapter we will describe a simple template
that creates the reverse complement of a
[FASTA](http://en.wikipedia.org/wiki/FASTA_format) file using the
[EMBOSS](http://emboss.sourceforge.net/)\citep{Ric00}
[revseq](http://emboss.sourceforge.net/apps/release/6.1/emboss/apps/revseq.html)
utility

#Definition

The definition is a list of variables defining what your template does
and giving Moa information on how to use this template.

## Describing the new template

The following variables define what your template does. These
variables are used in generating the help files, the manual and the
website.

  Identifier         Description
-----------------    ---------------------------------------------------
        moa_title    The title for this template
  moa_description    A short description of this template


Example:

     moa_title = Reverse Complement
     moa_description = This Moa template takes a set of      \
         input FASTA sequences and determines the reverse    \
         complement using the EMBOSS revseq utility.

Note: 

* Lines are allowed to break over multiple lines, but the
previous line must end with a backslash. No spaces are allowd after the backslash and the new line must be indented (with at least one space).

#Implementation
