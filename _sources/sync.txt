Synchronizing jobs
==================

It is quite often usefull to repeat a jobs on a number of different
input files. For simple operations, one liners, this ca be
accomplished using `moa map`. More complex operations, or those
requiring a template other than `map` can be replicated using job
syncronization. Assume you have a set of fastq libraries, each in it's
own directory::

    ./fq/set1/set1_1.fq
    ./fq/set1/set1_2.fq
    ./fq/set2/set2_1.fq
    ./fq/set2/set2_2.fq
    ./fq/set3/set3_1.fq
    ./fq/set3/set3_2.fq

And you want to run a bowtie alignment for each separately. The
approach to take is to create a directory containing all alignments::

    
    mkdir bowtie
    cd bowtie

and, in that directory, create one job running bowtie, in a directory
named **exactly** as the input directories::

    mkdir set1
    cd set1
    moa new bowtie -t 'run bowtie for {{_}}'

Note the magic variable `{{_}}`. This variable is replaced by the name
of the current directory. So when running `moa show`, the title would
show up as "run bowtie for set1". This magic variable can be used in
all variables, and we'll use it here to set this job up in such a way
that it can be reused for the other datasets::

   set moa fq_forward_input='../../fq/{{_}}/*_1.fq'
   # .. configure the remaining variables

Now - we replicate this directory in the following manner. We'll move
one directory up, to the `bowtie` directory, and create a `sync` job::
    
    cd ..
    moa new sync -t 'run bowtie for all fq datasets'
    moa set source=../fq/

The sync template keeps directories synchronized, based on the
`source` directory. If you now run `moa run` in the `bowtie`
directory, two more directories will be created: `set2` and `set3`,
each containing a verbatim copy of the original bowtie job created. 

If, at a certain moment you obtain more fastq datasets::

    ./fq/set4/set4_1.fq
    ./fq/set4/set4_2.fq

you can repeat `moa run` in the `./bowtie` sync directory, and a new
directory will be created. Note that the `sync` template will not
remove directories. Also if you want to update the configuration of
the syncronized bowtie jobs, you only need to change the configuration
in one directory, run `moa run` again in the `./bowtie` directory and
the configuration is synchronized across all jobs.
    







   

    

