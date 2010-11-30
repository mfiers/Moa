bowtie
------------------------------------------------

**Bowtie** - Run BOWTIE on an set of input files (query) vs a database index.

Commands
~~~~~~~~

**clean**
  Remove all job data, not the Moa job itself, note that this must be implemented by the template.


**run**
  *no help defined*





Filesets
~~~~~~~~




**input** - Input files for bowtie

  | *type*: `input`
  | *category*: `input`
  | *optional*: `False`
  | *extension*: `fastq`
  | *glob*: `{}`






Parameters
~~~~~~~~~~



**basename** - basename for generating the merged, sorted and indexed files
  | *type*: `string`
  | *default*: `all`
  | *optional*: `True`



**db** - The bowtie database to use. It is allowed to define one of the bowtie database files (.[0-9].ebwt).
  | *type*: `file`
  | *default*: ``
  | *optional*: `True`



**extra_params** - extra parameters to feed bowtie
  | *type*: `string`
  | *default*: ``
  | *optional*: `True`



**forward_suffix** - Last part of the sequence name identifying a file with forward reads
  | *type*: `string`
  | *default*: `_1`
  | *optional*: `True`



**input_format** - Format of the input files
  | *type*: `set`
  | *default*: `fastq`
  | *optional*: `True`



**insertsize** - Expected insertsize
  | *type*: `float`
  | *default*: `5000`
  | *optional*: `True`



**insertsize_max** - Max insertsize for a paired alignment
  | *type*: `float`
  | *default*: `10`
  | *optional*: `True`



**insertsize_min** - multiplier determining the minimal acceptable value for two paired reads to be apart. If the bowtie_insertsize is 10000 and this parameter is set at 0.8, than reads that are closer together than 8000 nt are rejecte
  | *type*: `float`
  | *default*: `0.1`
  | *optional*: `True`



**insertsize_sed** - SED expression to filter the expected insertsize from the input file name
  | *type*: `string`
  | *default*: ``
  | *optional*: `True`



**msi** - Merge, sort and index? If *T* use samtools to merge all bamfiles into one, sort them and create an index
  | *type*: `set`
  | *default*: `F`
  | *optional*: `True`



**output_format** - Format of the output file
  | *type*: `set`
  | *default*: `bam`
  | *optional*: `True`



**paired_ends** - perform a paired end analysis. If so, the input files are expected to be of the form *_1.fastq and  *_2.fastq
  | *type*: `set`
  | *default*: `F`
  | *optional*: `True`



**reverse_suffix** - Last part of the sequence name identifying a file with reverse reads
  | *type*: `string`
  | *default*: `_2`
  | *optional*: `True`



**title** - A name for this job
  | *type*: `string`
  | *default*: ``
  | *optional*: `False`



Other
~~~~~

**Backend**
  gnumake
**Author**
  Mark Fiers
**Creation date**
  Wed Nov 10 07:56:48 2010
**Modification date**
  Wed Nov 10 07:56:48 2010



