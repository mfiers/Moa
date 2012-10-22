bwa_samse
------------------------------------------------




    Generate alignments in SAM format given single end reads, using both 'bwa samse'.



Commands
~~~~~~~~

**clean**
  Remove all job data, not the Moa job itself
  
  
**run**
  run bwa samse
  
  

Filesets
~~~~~~~~


**fq_input**
  fastq input file





**output_bam**
  output bam file


  | *type*: `map`
  | *source*: `fq_input`
  | *category*: `output`
  | *optional*: `{}`
  | *pattern*: `./*.bam`




**sai_input**
  sai input directory - filenames must correspond to the fastq input files


  | *type*: `map`
  | *source*: `fq_input`
  | *category*: `input`
  | *optional*: `False`
  | *pattern*: `*/*.sai`





Parameters
~~~~~~~~~~



**db**
  bwa database to align against

  | *type*: `string`
  | *default*: ``
  | *optional*: `False`



**max_aln_out**
  Maximum number of alignments to output in the XA tag for reads paired properly

  | *type*: `integer`
  | *default*: `3`
  | *optional*: `True`



miscellaneous
~~~~~~~~~~~~~

**Backend**
  ruff
**Author**
  Yogini Idnani, Mark Fiers
**Creation date**
  Wed Nov 25 17:06:48 2010
**Modification date**
  unknown
