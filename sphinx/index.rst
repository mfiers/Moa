Welcome to Moa!
###############

*Command line workflows in bioinformatics*

Moa aims to assist a bioinformatician to organize, document, share,
inspect, execute and repeat workflows in a command line environment -
without losing any of the flexibility of the command line (see
:ref:`goals`).

*NOTE: The software (and manual) are under development. Things might
 still change.*


Introduction
============

These days, generating massive amounts of data is an everyday element
of biological research; and almost all projects have a computational
biology, or bioinformatics, components. Such embedded work commonly
consists of chaining a number of 3\ :sup:`rd` party tools together,
often with some data manipulation in between the steps. It is
important to have such projects properly organized, particularly when
a projects grows bigger.

There are many different ways to organize a bioinformatics
project. Many bioinformaticians use the command line, scripts or
`Makefiles <https://www.gnu.org/software/make/>`_ to organize and
automate their work. This approach has obvious advantages, most
importantly flexibility. With almost any approach, meticulous care
needs to be taken to keep a project well organized and documented. If
this is not done, it is easy to lose track, certainly when others have
to try to make sense of your project.

Moa hopes to make meticulous organization of a command line project
much less of a burden - leaving you to focus on the fun parts.


Thoughts on workflow organization
=================================

Most (bioinformatics?) projects start small, and grow over time. From
that perspective it is advisable to give the organization of your
project some thought on forehand.

When using Moa a workflow resides in a directory tree, with each
directory containing the separate analysis steps. A Moa job is linked
to a directory, and one directory can contain only Moa job. In- and
output data of each analysis typically resides in the same directory
structure. Having bot structure and data as regular files on your file
system makes a workflow extremely accessible. It is however important
that the directory structure represent the workflow in a logical
manner.

There are likely multiple ways of achieving a healthy organization of
a bioinformatics (Moa) project, we proposes the following
organization:


-  On the highest levels organize your project according to
   fundamental divisions in the project or data source. For example,
   if you work with data from multiple organisms, that might be a good
   top level division.

-  On lower levels start organizing your annotation pipeline. Since
   most



Table of contents:
==================

.. toctree::
   :maxdepth: 1
   :glob:

   goals
   install
   intro
   intro2
   configuration
   execution
   filesets
   coretemplates
   sync
   git
   contribute
   write_template
   commands/index
   templates/index
   api/index


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

