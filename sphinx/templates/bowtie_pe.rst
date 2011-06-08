bowtie_pe
------------------------------------------------




    Run BOWTIE on an set of input files (query) vs a database index.



Commands
~~~~~~~~

**clean**
  Remove all job data, not the Moa job itself
  
  
**report**
  Create a report on the results
  
  
**run**
  *no help defined*
  
  
  **run** delegates execution to: **run2, report**
  
**run2**
  Execute bowtie in paired-end mode
  
  

Filesets
~~~~~~~~


**db**
  The (basename of the) bowtie database to use.


  | *type*: `single`
  | *category*: `prerequisite`
  | *optional*: `False`
  | *pattern*: `../20.bowtiedb/db`




**fq_forward_input**
  fastq input files directory - forward





**fq_reverse_input**
  fastq input files directory - reverse


  | *type*: `map`
  | *source*: `fq_forward_input`
  | *category*: `input`
  | *optional*: `True`
  | *pattern*: `*/*_2.fq`




**output**
  Bam output file


  | *type*: `map`
  | *source*: `fq_forward_input`
  | *category*: `output`
  | *optional*: `{}`
  | *pattern*: `./*.bam`





Parameters
~~~~~~~~~~



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



**max_insertsize**
  Maximum allowed insertsize

  | *type*: `integer`
  | *default*: `250`
  | *optional*: `True`



**min_insertsize**
  Minimum allowed insertsize

  | *type*: `integer`
  | *default*: `1`
  | *optional*: `True`



**orientation**
  orientation of the reads, allowed values are fr, rf, ff

  | *type*: `{}`
  | *default*: `fr`
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
