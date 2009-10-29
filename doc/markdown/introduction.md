**NOTE: both the software and the manual are under heavy
development. Expect things to change.**

Moa is a set of tools build around [GNU
make](http://www.gnu.org/software/make) \citep{Gnumake} that
facilitates the use of GNU make in bioinformatics data analysis.

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
this [refs..], each with its own perks. A surprising number of
bioinformaticians, however, use either the command line or small,
tailor-made, scripts since that gives them ultimate flexibility. Using
scripts has as advantage that it is easy to repeat an analysis by
rerunning the script. Such a script could be written in any language
(Bash, Perl, Python) but could also be a custom Makefile.

...

Moa wraps a set of common bioinformatics tools as Makefiles. Using Moa
gives you a:

* A uniform interface; all Moa makefiles use a central library that
  provides a uniform, command line, interface to configuring and
  executing jobs.

* An easy way to track and repeat a set of analyses. Using Moa makes
  the creation of organized analysis structures easy.

* Interaction; templates are designed to interact with each other and
  make it easy to build pipelines using the Moa makefiles as building
  blocks.

* Parallel execution; Gnu make facillitates (limited) parallel
  execution of jobs. There is nothing however, that prevents
  integrations with a third party cluster solution such as Hadoop or
  SGE.
 
Apart from a set of template Makefiles, the Moa contains several other

* moaBase; a central library describing a number of central routines used by
	all Makefiles

* The "moa" helper script; a frontend to using Moa.

* Additional helper scripts; several of the template files require
	helper scripts that are part of the moa package.

## Example session 

The best way to understand how to use Moa is a sample session.

We'll start by creating directories to hold the data and analysis
structure:
 
    mkdir introduction
    cd introduction
    mkdir 10.download
    cd 10.download

We've created a directory called `introduction` to store the
introductory tutorial. Within this directory we'll organize the
components of our sample analysis. Moa doesn't enforce any
organization your analysis pipeline, but expects the user to do so.
An easy way to do this is by employing a logical directory
structure. Hence, the directory describing the first step in our
analysis, downloading data from NCBI, is prefixed with a `10.`. Later
steps will use higher numbers. 

We have will now created a new folder to hold a genome sequence we are
about to download and set up the Moa makefile to actually do the
download.

    mkdir 10.genome
    cd 10.genome
    moa new 'download ecoli from NCBI' ncbi
	
Note that we use the a utility script called `moa`. This script takes
some general tasks around running Moa that cannot be done using
Makefiles. In this case, calling `moa new` a Moa Makefile is
created. The arguments of `moa new` are a (descriptive) title and
`ncbi`. The latter defining a template Makefile that describes how to
download data from NCBI. 

Before you can execute the Makefile you have to set parameters telling
Moa what you want to download. Running `make help` gives you an
overview of all the parameters that you can set. In the case of an
`ncbi` Moa Makefile, there are two parameters that really need to be
set: `ncbi_db` and `ncbi_query`. The other variables can be guessed.

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

