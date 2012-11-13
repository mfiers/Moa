Quick start
-----------

(note, to fully use the blast template - you will need the
`blastReport` script from the `Blue Ringed Octopus
<https://github.com/mfiers/Blue-Ringed-Octopus>`_ repository).

 The best way to understand how Moa can help to organize a command
line bioinformatics project is by an example.

Each Moa workflow consists of separate Moa jobs. An important feature
of Moa is that each Moa job resides in a directory, and each directory
can hold only *one* Moa job. A workflow is organised as a directory
tree, where the structure of the directory tree reflects the structure
of the project. This will (hopefully) stimulate a user to break a
workflow down into atomic parts, which will be beneficial to the
organization and coherence of a workflow. So, starting a Moa project
starts with creating a directory to hold the workflow::

    $ mkdir test.project
    $ cd test.project
    $ mkdir 00.proteins

    ## copy some protein sequences in 00.proteins

    $ mkdir 10.blast
    $ cd 10.blast

The order of steps can be ordered by prefixing directory names with a
number. Note that this not enforced by Moa. Once a directory is
created, a Moa job can be created (see :ref:`command_moa_new`)::

    $ moa new blast -t "demo run"

All interaction with Moa is done through a single command: `moa`. It
is, at all times, possible to get help on the use of the `moa` command
by invoking `moa -h` or `moa --help`. The command above creates a
`BLAST <http://blast.ncbi.nlm.nih.gov/>`_ job titled "demo run" in the
current directory. All Moa related files are stored in a (hidden)
sub-directory named `.moa` (go and have a look!).  A Moa job consists,
amongst others, of a configuration file (`.moa/config`) and a number
of template files (`.moa/template` and/or `.moa/template.d/*`). All
template files are copied into the `.moa` directory. This ensures that
a workflow remains the same over time, even if the templates are
updated. If you want to copy the latest version of a template to a Moa
job, use :ref:`command_moa_refresh`.

Moa also tries to assist in embedding documentation. In the above
command line the `-t` parameter sets a mandatory project title (a job
won't execute without a title). Moa also automatically records a
changelog (in `.moa/doc/change`). You can add your own changelog
messages by using the `-m` argument (before the command!) or by using
:ref:`command_moa_change`. Additionally, you can keep a "blog"
(:ref:`command_moa_blog`) for a higher level record on the development
of the work, and a "readme" (:ref:`command_moa_readme`) to create a
document for each job.

Back to the blast job - it is obviously not enough to tell Moa to do a
BLAST analysis. Some extra information is necessary (see
:ref:`command_moa_set`)::

    $ moa set db=/data/blast/db/nr

A few points are important to note: do not use spaces around the `=`
sign. If you want to define a parameter with spaces, use quotes
(`key="value with spaces"`), and be very aware of bash expansion. A
safer way to enter parameters is by running `moa set db` and Moa will
query you for the value (note that in both cases you can use
tab-completion).

If you want to check what the parameters are, you can use
:ref:`command_moa_show`.  which will give you a list of parameters
known to Moa::

    $ moa show
    db         l.M  /data/blast/db/nr
    input      d.M  */*.fasta
    jobid      s.o  blast
    title      l.M  demo run
	...

Note the variable `db` and `title`, which were set earlier. If you run
`show -a`, more parameters will be revealed, amongst which is
`program`. The flags between the variable key and value are explained
in: :ref:`command_moa_show`.

We will now set two more variables::

    $ moa set program=blastp
    $ moa set input=../00.proteins/*.fasta

The last statement defines the input files to blast. Once all is set
you can actually run (see :ref:`command_moa_run`) the BLAST analysis
with::

    $ moa run

Moa now performs the BLAST analysis on each of the input files. The
output can be found in the `out` sub-directory. As an extra, the Moa
`blast` template generates a `blast_report` file with simple one line
report for the best five hits of each query sequence.

To illustrate how easy it is to embed extra command lines into your
workflow, we will check for the presence of any `dicer` genes in the
query set by employing `grep`::

    $ grep -i dicer blast_report

To embed this in the workflow, execute::

    $ moa set postcommand

and, at the prompt enter::

    postcommand:
    > grep -i dicer blast_report > dicer.out

If you now rerun `moa`, the BLAST job will not be repeated, but the
`postcommand` will be executed and a `dicer.out` file will be
generated. (note, there is also a `precommand`)


