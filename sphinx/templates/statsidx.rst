statsidx
------------------------------------------------



::
    Retrieve and print stats from BAM file to an index file


Commands
~~~~~~~~

**clean**
  Remove all job data, not the Moa job itself


**run**
  run samtools idxstats





Filesets
~~~~~~~~




**input**::
    bam input files directory - forward files

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
  | *source*: `input`
  | *category*: `output`
  | *optional*: `{}`
  | *extension*: `{}`
  | *glob*: `{}`
  | *dir*: `{}`






Parameters
~~~~~~~~~~



**default_command**::
    command to run for this template

  | *type*: `{}`
  | *default*: `run`
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
  Wed Dec 08 17:06:48 2010
**Modification date**
  1291933991.11



