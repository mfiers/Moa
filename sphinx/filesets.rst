Filesets
========

Filesets are an important part of Moa - they are used to define input
and output files for Moa jobs. In principle, a fileset is not much
more than a collection of files. They are three different types:

Types
-----

Type "set"
..................

A "set" fileset is given a filesystem `glob
<https://en.wikipedia.org/wiki/Glob_%28programming%29>`_, checks the
filesystem and returns a list of files that conform to the glob
pattern. Type "set" filesets are typically used to define input of a
Moa job. A "set" fileset can (currently) contain only one `*`
wildcard. A correct example would be::

    /data/sequences/*.fasta

This glob does exactly what you expect. Lets assume that there are
three sequences in this directory, the set would contain three
filenames::

    /data/sequences/input_01.fasta
    /data/sequences/input_02.fasta
    /data/sequences/input_03.fasta

More complex patterns, and wildcards other than `*` are not supported
(yet). Each Moa job can have at most one "set" fileset.

Type "map"
..................

A "map" fileset converts a "set" fileset (the source) to a related
fileset, typically to calculate the output of Moa job. A "map" fileset
must be linked to "set" fileset and uses a glob like pattern to
convert the input "set" fileset to the resulting fileset. For example,
if we take the example fileset defined above, and apply the following
pattern::

    ./*.output

we would end up with the following "map" fileset::

    ./input_01.output
    ./input_02.output
    ./input_03.output

A potential pitfall is the following situation, where we have a "set"
fileset defined as follows::

    /data/sequences/input_*.fasta

This would result in exactly the same fileset as above. But if we now
apply the same "map" pattern, the resulting output fileset would be::

    ./01.output
    ./02.output
    ./03.output

This is because the `*` from the "set" glob maps the the `*` in the
"map" pattern, the rest is omitted. This can be useful, for example if
you would be using this in a Blast job, you could specify the
following "map" pattern::

    ./blast_*.out

which would result in the following output::

    ./blast_01.out
    ./blast_02.out
    ./blast_03.out

In the case of a "map" set it is allowed to use a second wildcard in
the pattern, for example::

    */blast_*.out

in which case the first wildcard is replaced with the original
path. In the above example this would result in::

    /data/sequences//blast_01.out
    /data/sequences//blast_02.out
    /data/sequences//blast_03.out

(note . you might not want to do this)

Type "single"
.............

Is a very simple fileset, pointing to a single file. No wildcards are
allowed.

Categories
----------

Moa has to keep track (using Ruffus) of in- and output of a job - it
does this by tracking filesets. The category defines in a file(set) is
considered "input", "output" or a "prerequisite". In- & output speaks for
itself, a prerequisite is also considered input (i.e. if it changes
the job will be repeated), but is typically kept out of the one-on-one
file mapping that takes place for in- and output files.

Defining filesets
-----------------

If you are developing a template, there is whole section devoted to
filesets. The following example is taken from the Moa BLAST template,
and contains almost everything that you will come across::

    filesets:
	  db:
	    category: prerequisite
	    help: Blast database
	    optional: false
	    pattern: '*/*'
	    type: single
	  input:
	    category: input
	    help: Directory with the input files for BLAST, in Fasta format
	    optional: false
	    pattern: '*/*.fasta'
	    type: set
	  outgff:
	    category: output
	    help: GFF output files
	    optional: true
	    pattern: gff/*.gff
	    source: input
	    type: map
	  output:
	    help: XML blast output files
	    category: output
	    optional: true
	    pattern: out/*.out
	    source: input
	    type: map

Most of this speaks for itself. A few things to note are:

* Both "outgff" and "output" are category "output", type "map", filesets
  mapping to the same input, type "set", fileset. This is common
  practice. If you have a look at the map22 template, you can even see
  an example of category "input", type "map" fileset.
* If a fileset has reasonable default patterns (values) (typically
  goes for output fileset), it is possible to make them optional.
* Please specify a good help text

..  LocalWords:  fileset
