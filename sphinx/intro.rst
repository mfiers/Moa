Quick start
-----------

The best way to understand how Moa can help to organize a command line
bioinformatics project is by an example.

Each Moa workflow consists of separate Moa jobs. An important feature
of Moa is that each Moa job resides in a directory, and each directory
can hold only one Moa job. A workflow is organised as a directory
tree, where the structure of the directory tree reflects the structure
of the project. This (hopefully) stimulates a user to break a workflow
down into atomic parts, which is typically beneficial to the
organization and coherence of a workflow. So, Starting a Moa project
starts with creating a directory to hold the workflow::

    $ mkdir test.project
	$ cd test.project
    $ mkdir 00.proteins

    ## copy some protein sequences in 00.proteins
    $ mkdir 10.blast
	$ cd 10.blast

The order of steps is easily ordered by prefixing directory names with
a number. Note that this not enforced by Moa; any alphanumerical
organization would work. Once a directory is created, a Moa job can be
created::

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

Obviously, telling a Moa job to do a BLAST analysis is not enough, some extra information will need to be given::

    $ moa set db=/data/blast/db/nr

A few things could be noted here. Important is that you do not use spaces around the `=` sign. If you want to define a parameter with spaces, use quotes (`key="value with spaces"`), and be aware of bash interpretation. A safe way of entering complex parameters is by running `moa set db` and Moa will query you the value.

Another point is that Moa does not give you a response. You can check the current job configuration using `moa show`, which would at this moment result in something resembling::

    db     L /data/blast/db/nr
    input  E (undefined)
    jobid  L blast
    title  L demo run

Note the variable `db` and `title`, which were set earlier. If you run `show -a`, more parameters will be revealed, amongst which is `program`. We will now set two more variables::

    $ moa set program=blastp
    $ moa set input=../00.proteins/*.fasta

The last statement defines the input files to blast. Once all is set you can actually run the BLAST analysis with::

    $ moa run

Now Moa performs the BLAST analysis on the input files. The output can be found in the `out` sub-directory. As an extra, the Moa `blast` template generates a `blast_report` file with simple one line report for the best five hits of each query sequence. If you, for example, would like to check for the presence of dicer genes in your query set, you could `grep` this file::

    $ grep -i dicer blast_report

Command line operation of data files can be very powerful, and this would be a typical operation for a command line bioinformatician. Moa lets you capture this and thus make it a part of the pipeline. Try::

    $ moa set postcommand

and, at the prompt enter::

    postcommand:
    > grep -i dicer blast_report > dicer.out

If you now rerun `moa`, the BLAST job will not be repeated, but the `postcommand` will be executed and a `dicer.out` file will be generated. (note, there is also a `precommand`)

