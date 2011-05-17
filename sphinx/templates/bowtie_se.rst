bowtie_se
------------------------------------------------




    Run BOWTIE on an set of input files (query) vs a database index.



Commands
~~~~~~~~

**clean**
  Remove all job data, not the Moa job itself, note that this must be implemented by the template
  
  
**run**
  *no help defined*
  
  

Filesets
~~~~~~~~


**fq_input**
  fastq input files directory





**output**
  Bam output file


  | *type*: `map`
  | *source*: `fq_input`
  | *category*: `output`
  | *optional*: `{}`
  | *pattern*: `./*.bam`





Parameters
~~~~~~~~~~



**ebwt_base**
  The (basename of the) bowtie database to use.

  | *type*: `string`
  | *default*: `{}`
  | *optional*: `False`



**extra_params**
  extra parameters to feed to bowtie

  | *type*: `string`
  | *default*: ``
  | *optional*: `True`



**input_format**
  Format of the input files

  | *type*: `set`
  | *default*: `fastq`
  | *optional*: `True`



**output_format**
  Format of the output file

  | *type*: `set`
  | *default*: `bam`
  | *optional*: `True`



miscellaneous
~~~~~~~~~~~~~

**Backend**
  ruff
**Author**
  Yogini Idnani, Mark Fiers
**Creation date**
  Wed Nov 10 07:56:48 2010
**Modification date**
  Wed Nov 10 07:56:48 2010
