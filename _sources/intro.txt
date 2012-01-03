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
untraceable unless measures are taken.

*Moa* aims to assist in organizing, automating and maintaining a
command line bioinformatics project without loss of flexibility.

Example
-------

The best way to understand how Moa can help you to achieve this is by
an example. A Moa workflow consists of separate Moa jobs. A workflow
is typically organised as a directory tree, where the structure of the
tree reflects the structure of the project. So, Starting a Moa project
starts with outlining a directory structure to contain the workflow::

    $ mkdir test.project && cd test.project
    $ mkdir 00.proteins
    
    ( copy or link some protein sequences into 00.proteins )
   
    $ mkdir 10.blast
    $ cd 10.blast

An important feature of Moa is that each separate analysis step is
contained within a separate directory. Two Moa jobs never share a
directory. This forces a Moa user to break a workflow down to atomic
parts, which is typically beneficial to the organization and coherence
of a workflow. The order of steps is easily ordered by prefixing
directory names with a number. Note that these prefixes are not
enforced by Moa; any alphabetical organization would work as
well. Once a directory is created, a Moa job can be created::

    $ moa new blast -t "demo run"

All interaction with Moa is done through a single command: `moa`. It
is, at all times, possible to get help on the use of the `moa` command
by invoking `moa --help`. The command above creates a `BLAST` job
titled "demo run" in the current directory. All Moa related files are
stored in a (hidden) sub-directory names `.moa` (have a look!).  A Moa
job consists, amongst others, of a configuration file and a number of
template files. All template files are copied into the `.moa`
directory. This ensures that a workflow remains the same over time,
even if the templates are updated (`moa refresh` would update a
template to the latest version).

Another topic in which Moa tries to help is by embedding (some)
documentation. In the above command line the `-t` parameter sets a
mandatory project title (a job won't execute without a title).

Obviously, telling a Moa job to do a BLAST analysis is not enough,
some variables will need to be set::

    $ moa set db=/data/blast/db/nr

A few things could be noted here. Important is that you do not use
spaces around the `=` sign. If you want to define a parameter with
spaces, use quotes (`key="value with spaces"`), and be aware of bash
interpretation. A safe way of entering complex parameters is by
running `moa set db` and Moa will query you the value.

Another point is that Moa does not give you a response. You can check
the current job configuration using `moa show`, which would at this
moment result in something resembling::

    db     L /data/blast/db/nr
    input  E (undefined)
    jobid  L blast
    title  L demo run

Note the variable `db` and `title`, which were set earlier. If you run
`show -a`, more parameters will be revealed, amongst which is
`program`. We will now set two more variables::

    $ moa set program=blastp
    $ moa set input=../00.proteins/*.fasta
    
The last statement defines the input files to blast. Once all is set
you can actually run the BLAST analysis with::

    $ moa run

Now Moa performs the BLAST analysis on the input files. The output can
be found in the `out` sub-directory. As an extra, the Moa `blast`
template generates a `blast_report` file with simple one line report
for the best five hits of each query sequence. If you, for example,
would like to check for the presence of dicer genes in your query set,
you could `grep` this file::

    $ grep -i dicer blast_report

Command line operation of data files can be very powerful, and this
would be a typical operation for a command line bioinformatician. Moa
lets you capture this and thus make it a part of the pipeline. Try::

    $ moa set postcommand

and, at the prompt enter::

    postcommand:
    > grep -i dicer blast_report > dicer.out

If you now rerun `moa`, the BLAST job will not be repeated, but the
`postcommand` will be executed and a `dicer.out` file will be
generated. (note, there is also a `precommand`)

