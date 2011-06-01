**NOTE: both the software and the manual are under development. Things
  might change.**

Introduction
============

These days, generating massive amounts of data is an everyday element
of biological research; and almost all projects have a bioinformatics
components. Such embedded bioinformatics work commonly consists of
chaining a number of 3\ :sup:`rd` party tools together, often with
some data manipulation in between the steps. It is important to have
such projects properly organized, particularly when a projects grows
bigger.

There are many different ways to organize bioinformatics
projects. Many bioinformaticians use the command line or tailor made
scripts to organize and automate their work. This approach has obvious
advantages, most importantly flexibility. Potential downsides to
scripting are that a project easily becomes disorganized and
untrackable unless measures are taken.

***Moa** aims to assist in organizing, automating and maintaining a
command line bioinformatics project without loss of flexibility.*

The best way to understand how Moa can help you to achieve this is by
an example. Running Moa typically starts with creating a directory to
hold an analysis job, or workflow::

    mkdir 10.blast
    cd 10.blast


An important feature of Moa is that each separate analysis step is
contained within a separate directory. Two Moa jobs never share a
directory. This forces the Moa user to break a workflow down to atomic
parts, which is typically beneficial to the organization and coherence
of a workflow. The order of steps is easily ordered by prefixing
directory names with a number. Note that these prefixes are not
enforced by Moa; any alphabetical organization suffices. Once a
directory is created, a Moa job can be created::

    moa new blast -t "demo run"

All interaction with Moa is done through a single command: `moa`. It
is, at all times, possible to get help on the use of the `moa` command
by invoking `moa --help`. The command above creates a `BLAST` job
title "demo run" in the current directory. All Moa related files are
stored in a (hidden) subdirectory names `.moa` (have a look). 

A Moa job consists, amongst others, of a configuration file and a
number of template files. All template files are copied into the local
`.moa` directory. This ensures consistency of a workflow, even if the
templates are updated (`moa refresh` updates a template to the latest
version).

Obviously, telling a job to do a BLAST analysis is not enough, some
variables will need to be set::

    moa set db=/data/blast/db/nr

Note that Moa does not give you a response. You can check the current
job configuration using `moa show`, which would at this moment result
in something resembling::

    db      /data/blast/db/nr
    eval    1e-10
    gff_blasthit    F
    gff_source      BLAST
    input           (undefined)
    nohits  50
    nothreads       2
    outgff  gff/*.gff
    output  out/*.out
    postcommand
    precommand
    program blastn
    project
    title   demo run

Note the variable `db` and `title`, which were set earlier, amongs a
list of other variables. We will set two more variables::

    moa set program=blastp
    moa set input=/data/00.seq/*.fasta
    
The last statement defines the input files to blast. Once all is set
you can actually run the BLAST analysis with::

    moa run

Now Moa performs the BLAST analysis on the input files

``/data/blast/db/nt``. BLAST output files (XML) are generated and
converted to GFF (GFF conversion is an extra of the template, not part
of the BLAST suite). The one to last statement is probably most
typical of the flexibility provided by Moa; it is a single shell
commmand that will be executed after BLAST is executed (there is a
corresponding ``moa_preprocess``). This shell comamand filters all
BLAST hits that have the word "polymerase" in their description into a
separater GFF file.


Moa aims to do the following things:

-  *Organize a project*: Each Moa job must be located in its own
   directory. It is possible to automatically execute a directory tree
   of Moa jobs. Proper use of these features will result in a logical
   project structure.
- *Create reusable building blocks*: Moa templates are GNU Makefiles
   that follow a set of conventions. It is easy to implement new
   building blocks. (see chapter X).
-  *Document*: It is possible to add meta-data such as a title and
   description to each Moa job, making it easy to
-  *Provide a uniform interface*: Moa allows you to operate your
   project almost exclusively using a single command (conveniently
   called ``moa``).


Example session
---------------

The best way to understand how to use Moa is a sample session.

We'll start by creating directories to hold the data and analysis
structure:

::

    mkdir introduction
    cd introduction

We've created a directory ``introduction`` for the tutorial. Within
this directory we'll organize the components of our analysis. We
want to initialize this directory so that it becomes a part of this
Moa pipeline. This is useful later, if we want to run all analysis
at once. To do this, run:

::

    moa new project -t 'Introduction'

The ``moa new`` command is used to create new moa jobs. In this
case we create a job with the template "project". In itself this
template does not do anything but serves to group new projects. The
``-t`` parameters assigns a title to this Moa job. We will now
create a new directory to hold the first step of the pipeline:

::

    mkdir 10.download    
    cd 10.download
    moa new

Moa does not dictate a directory structure for your analysis
pipeline, but to make full usage of Moa it is advisable to create a
logical organization. Two important features of Moa that relate to
this are:


-  Each moa job is contained in one directory. Output files of a
   job are typically stored in that directory. It is not possible to
   have more than one Moa jobs in a directory.
-  Moa is able to automatically execute all jobs in a directory and
   the underlying sub-directories (using ``moa all``).

If properly used, these two features force a logical, modular,
project structure. To assign an order to the steps inside a
directory it is possible to prepend a number to the directory name
(i.e. "10."). Note that Moa sorts directories alphabetically and
not numerically

We will now created a new folder to hold a genome sequence we are
about to download and set up the Moa job to actually do the
download.

::

    mkdir 10.genome
    cd 10.genome
    moa new -t 'download a potato BAC' ncbi

Here we create a Moa job to download a sequence from
`NCBI <http://www.ncbi.nlm.nih.gov>`_ by using the "ncbi" template.
Once a Moa job is instantiated you can run ``moa help`` to get some
information on how to use this template

|moa help| Note that if you want help on how to use the moa itself,
you should use ``moa --help``

Before you can get the data from NCBI, you will have to tell Moa
what you want to download. This is easy if you know the Genbank
accession numbers. In this case we'll download the nucleotide
sequence (from the database "nuccore") with the accession id
AC237669.1

::

    moa set ncbi_db=nuccore 
    moa set ncbi_query=AC237669.1

You can check if the parameters are set correctly by running
``moa show``. This should come back with the following text: title
download a potato BAC ncbi\_query AC237669.1 ncbi\_db nuccore
ncbi\_sequence\_name

If everything seems fine, you can run this job:

::

    moa

Or, you could also have used ``moa run``. It is possible that you
get an error message notifying that "wget" or "xml\_grep" cannot be
found. Most, properly written, Moa templates do prerequisite
checking if necessary. If either of these tools is missing, you
will need to install them first (possibly by running
``sudo apt get install wget`` or
``sudo apt-get install xml-twig-tools``, or ask your system
administrator)

If Moa runs, quite a lot of output is generated. If things go
wrong, there is probably a clue to why it did not work in this
output. If the Moa job is successful, the last line should be "Moa
finished - Succes!". If you do an ``ls`` you now see a ``fasta``
directory with one fasta file. This fasta file contains the
downloaded genome.

Now we can start doing things with the downloaded sequence. To see
what other templates are available, try ``moa list``.


.. |moa help| image:: images/screenshot_moa_help.png


-------------------

.. [BLAST] Altschul SF, Gish W, Miller W, Myers EW, Lipman DJ. Basic local alignment search tool. J Mol Biol. 1990 Oct 5;215(3):403-10. PubMed PMID: `2231712 <http://www.ncbi.nlm.nih.gov/pubmed/2231712>`_.
