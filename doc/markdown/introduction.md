**NOTE: both the software and the manual are under development. Expect
  things to change.**

Moa is a set of tools aimed at organizing and automating a
bioinformatics analysis pipeline. The best way to understand what Moa
does is by a small example:

    moa new blast -t "run a demo"
    moa set blast_db=/data/blast/db/nt
    moa set blast_input_dir=../sequences
    moa run

In the first line, a new BLAST job (titled "run demo") is created in
the current directory. What really happens is that Moa creates a
Makefile (more about Makefiles later) based on a BLAST specific
template. The next two lines set BLAST specific parameters. In the
last line Moa is executed and comparies the sequences in the
`../sequences` directory against the database in `/data/blast/db/nt`
using BLAST. BLAST output files are generated in the current directory
and, additionally, GFF \citep{GFF} files.

Moa is build around [GNU make](http://www.gnu.org/software/make)
\citep{Gnumake} that facilitates building and reusing the use of GNU
make in bioinformatics data analysis.

GNU Make is developed to aid in compilation of software. Software
compilation usually involves the execution of many preprocessing,
compilation and linker steps, with different parameters and
interdependent of each other.

Gnu make is able to compile tens of thousands of files in large
software projects through a detailed description of exactly what
target files are to be created; from what source files; in what order;
and using which libraries. If, during development, a few source files
have changed, Gnu Make is able to repeat only the affected part of the
build process.

The description, used by Gnu Make, that describes the build process is
called a Makefile. The syntax of a Makefile is flexible enough to
allow Gnu Make to be used for practically any programming
language. Moreover, Gnu Make can be used to automate any series of
commands (as long as they can be executed from the command line). It
is therefore not only possible, but an excellent idea (not mine), to
use Gnu Make in bioinformatics projects (see: X, Y, Z)

A bioinformatics analysis is often a set of interdependent, standard,
steps (rather like compiling software). For example: (1) You take a
piece of genomic DNA; (2-4) perform a set of gene predictions; (5)
integrate the predictions and (6) run BLAST on the predicted genes.

There are, apart from using Makefiles, many different ways to automate
this [refs..], each with its advantages. A surprising number of
bioinformaticians, however, use either the command line or small,
tailor-made, scripts to retain ultimate flexibility. Using scripts has
as advantage that it is easy to repeat an analysis by rerunning the
script. Such a script could be written in any language (Bash, Perl,
Python) but could also be a custom Makefile.

...

Moa wraps a set of common bioinformatics tools as Makefiles. Using Moa
gives you a:

* A uniform interface; although Moa is based around Gnu Make, all
  commands are executed using the "moa" utility script. The "moa"
  script often just invokes Gnu Make but is able to handle a few extra
  cases where the use of Gnu Make is not possible.

* An easy way to track and repeat a set of analyses. 

* Interaction; the Makefile templates are designed to interact with
  each other and make it easy to build pipelines with the Moa
  makefiles as building blocks.

* Parallel execution; Gnu make facillitates (limited) parallel
  execution of jobs. There is nothing however, that prevents
  integrations with a third party cluster solution such as Hadoop or
  SGE.
 
## Example session 

The best way to understand how to use Moa is a sample session. 

We'll start by creating directories to hold the data and analysis
structure:
 
    mkdir introduction
    cd introduction

We've created a directory called `introduction` to store the
introductory tutorial. Within this directory we'll organize the
components of our sample analysis. We want to initialize this
directory so that it becomes a part of a moa pipeline. This is usefull
later, if we want to run all analysis at once. To do this, run:

    moa new -p introduction

The "moa new" command is used to create new moa jobs. In this case,
since it is the first the -p (or --project) parameter tells Moa that
this project is called "introduction". Moa uses a frontend script
(called moa) to provide uniform interaction with the system. We'll now
create a new directory to hold the first step of the pipeline:

    mkdir 10.download    
    cd 10.download
    moa new

Moa doesn't enforce any organization of an analysis pipeline, but
expects the user to do so.  An easy way to do this is by employing a
logical directory structure. Hence, the directory describing the first
step in our analysis: downloading data, is prefixed with a
`10.`. Later steps will use higher numbers. Note that "moa new" is
executed again, this time omitting the -p parameter. If the project
parameter is omitted, moa tries to resolve this by reading the moa
configuration in the parent directory.

We will now created a new folder to hold a genome sequence we are
about to download and set up the Moa makefile to actually do the
download.

    mkdir 10.genome
    cd 10.genome
    moa new -t 'download a potato bac' ncbi
	
This time we have added a new parameter to the 'moa new' invocation:
"ncbi".  This tells Moa that in this directory the "ncbi" template
should be used that allows easy downloading of information from
NCBI. We also provide, as a good practice, a descriptive title using
the -t (or --title) parameter. In general, once a moa makefile is
instantiated you can call "moa help" to get some information on how to
use this template:

    moa help

(Note that if you want help on how to use the moa frontend script, you
should use moa --help)

Before you can execute this job you have to tell what needs to be
downloaded. This is easy if you know the Genbank accession number. In
this case we'll download the nucleotide sequence (from the database
nuccore) with the accession id AC237669.1

   moa set ncbi_db=nuccore 
   moa set ncbi_query=AC237669.1

Moa will give a response indicating that it has set the two
parameters. You can also check the "moa.mk" file that stores job
specific parmaters or run:

   moa show


help` gives you an overview of all the parameters that you can set. In
the case of an `ncbi` Moa Makefile, there are two parameters that
really need to be set: `ncbi_db` and `ncbi_query`. The other variables
can be guessed.

Values for these parameters can, in this case, be found on the NCBI
website. Once you have a found a sequence the parameters can be
extracted from the URL. In this case, we will download a
***Lactobacillus*** genome from
[NCBI](http://www.ncbi.nlm.nih.gov/nuccore/NC_012214). The URL
(`http://www.ncbi.nlm.nih.gov/nuccore/NC_012214`) reveals the two
parameters necessary. They can be set with the following command:

    make set ncbi_db=nuccore ncbi_query=NC_004567

Nothing appears to have happened
however, check what parameters are set by running:

    make show

You should now see:

    ncbi_db	nuccore
    ncbi_query	NC_004567
    gfn_sequence_name	
    jid	moa_getFromNcbi_10.genome_??????????
    project	

There are a few more parameters here, you can ignore all of these now,
execpt for "jid". A "jid", or "job id" is a unique name that will be
used to track information on this job. It is important, particularly
if you're creating big projects, to set this to an understandable,
descriptive, but short value (without spaces!!), so we'll run an
additional `make set`:

    make set jid=lactobacillus.genome

This job is set up and can be executed now by running:

    make

This generates quite a lot of output. If things go wrong, there is
probably a clue to why in the output. If the Moa job is successful,
the last line should be "Moa finished - Succes!". If you do an `ls`
you now see a `fasta` directory with one fasta file. This fasta file
contains the downloaded genome.

Good, nice, but not very exciting. We'll now start doing something
with this data. For example, we could map the results from a 454 run
against this genome. Lets download a dataset from [NCBI's short read
archive](http://www.ncbi.nlm.nih.gov/Traces/sra/sra.cgi?):

    cd ..
    mkdir 20.454reads
    cd 20.454reads
	mkdir 10.download
	cd 10.download
    moa new lftp

Here we use a different template: lftp. We need to set a single
parameters (i.e. the location of the file to download). 

    make set lftp_url=ftp://ftp.ncbi.nlm.nih.gov/sra/static/SRX002/SRX002375/SRR011133.fastq.gz
    make set jid=lactobacillus.454.reads

again we can run `make` to download the data. After downloading we see
that an archive is downloaded. We have now two options - unpack it
manually or automate unpacking. We could do it manually. If the
project is a quick, one-off, this is probably not so bad. However, you
won't be able to completely rerun the analysis without having to think
what steps you did manually. Therefore, we'll now set something up to
also automate this. 

    cd ..
    mkdir 20.unpack
    cd 20.unpack
    moa new gather

The Moa "gather" template is probably not named very well. It's a very
flexible template that allows you to do many different things on a set
of input files (read the manual page). We'll set it up now to automate
the unpacking.

    make set g_input_dir=../10.download
    make set g_input_pattern=*.gz
   
These two lines define what files are used as input for the "gather"
step. The next parameter is a sed command that strips of the .gz
extension for the unpacked output file.

    make set g_name_sed='s/\.gz$//'

(Note that you must use ' quotes to prevent bash from expanding the $
sign as a variable!)

    make set g_process=`

