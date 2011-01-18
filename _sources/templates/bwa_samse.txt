bwa_samse
------------------------------------------------



::
    Generate alignments in SAM format given single end reads, using both 'bwa samse'.


Commands
~~~~~~~~

**clean**
  Remove all job data, not the Moa job itself


**run**
  run bwa samse





Filesets
~~~~~~~~




**fq_input**::
    fastq input file

  | *type*: `map`
  | *source*: `{}`
  | *category*: `input`
  | *optional*: `False`
  | *extension*: `{}`
  | *glob*: `{}`
  | *dir*: `{}`







**output**::
    {}

  | *type*: `map`
  | *source*: `fq_input`
  | *category*: `output`
  | *optional*: `{}`
  | *extension*: `{}`
  | *glob*: `{}`
  | *dir*: `{}`







**output_bam**::
    {}

  | *type*: `map`
  | *source*: `fq_input`
  | *category*: `output`
  | *optional*: `{}`
  | *extension*: `{}`
  | *glob*: `{}`
  | *dir*: `{}`







**sai_input**::
    sai input directory - filenames must correspond to the fastq input files

  | *type*: `map`
  | *source*: `fq_input`
  | *category*: `input`
  | *optional*: `False`
  | *extension*: `{}`
  | *glob*: `{}`
  | *dir*: `{}`






Parameters
~~~~~~~~~~



**db**::
    bwa database to align against

  | *type*: `string`
  | *default*: ``
  | *optional*: `False`



**default_command**::
    command to run for this template

  | *type*: `{}`
  | *default*: `run`
  | *optional*: `True`



**max_aln_out**::
    Maximum number of alignments to output in the XA tag for reads paired properly

  | *type*: `integer`
  | *default*: `3`
  | *optional*: `True`



**title**::
    A name for this job

  | *type*: `string`
  | *default*: ``
  | *optional*: `False`



Other
~~~~~

**Backend**
  ruff
**Author**
  Yogini Idnani, Mark Fiers
**Creation date**
  Wed Nov 25 17:06:48 2010
**Modification date**
  1291933989.07



