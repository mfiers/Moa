bowtie
------------------------------------------------

**Bowtie**


    Run BOWTIE on an set of input files (query) vs a database index.



Commands
~~~~~~~~

**clean**
  Remove all job data, not the Moa job itself, note that this must be implemented by the template
  
  
**run**
  *no help defined*
  
  

Filesets
~~~~~~~~


**input**
  Fasta/fastq input files for bowtie





**output**
  Output files


  | *type*: `map`
  | *source*: `input`
  | *category*: `output`
  | *optional*: `{}`
  | *pattern*: `./*.bam`





Parameters
~~~~~~~~~~



**db**
  The (basename of the) bowtie database to use.

  | *type*: `string`
  | *default*: `{}`
  | *optional*: `False`



**extra_params**
  extra parameters to feed bowtie

  | *type*: `string`
  | *default*: ``
  | *optional*: `True`



**input_format**
  Format of the input files

  | *type*: `set`
  | *default*: `fastq`
  | *optional*: `True`



miscellaneous
~~~~~~~~~~~~~

**Backend**
  ruff
**Author**
  Mark Fiers
**Creation date**
  Wed Nov 10 07:56:48 2010
**Modification date**
  Wed Nov 10 07:56:48 2010
