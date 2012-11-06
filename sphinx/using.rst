Creating a pipeline
===================

Guiding principles
------------------

Most (bioinformatics?) projects start small, and grow over time.
From that perspective it is advisable to give the organization of
your project some thought on forehand.

When using Moa the separate analysis steps of a pipeline each
reside in a directory. The output data of each analysis usually
resides in the same directory or a subdirectory thereof. Moa has
templates that assist in downloading and organizing data. This has
as result that all project data in a Moa project will be organized
in a directory tree on your filesystem. Such a tree must represent
both the data in logical way as well as the analysis pipeline
organization.

Although there are likely multiple ways of achieving a healthy
organization of a Moa project, this manual proposes the following
organization:


-  On the highest levels organize your project according to
   fundamental divisions in the project or data source. For example,
   if you work with data from multiple organisms, that might be a good
   top level division.

-  On lower levels start organizing your annotation pipeline. Since
   most


Setting up new jobs - ``moa new``
---------------------------------

Creating a new job is done with the ``moa new`` command.

Running a pipeline
==================

Running one job
---------------

Running a series of jobs
------------------------

(Something should be written here)

