bidibebla
------------------------------------------------

**Bidirectional best BLAST hit**

::
    Discover the bidirectional best blast hit between two sets of sequences


Commands
~~~~~~~~

**clean**
  Remove all job data, not the Moa job itself, note that this must be implemented by the template.


**run**
  generate a list of bidirectional best blast hits





Filesets
~~~~~~~~




**input**::
    Fasta input files

  | *type*: `map`
  | *source*: `{}`
  | *category*: `input`
  | *optional*: `False`
  | *extension*: `{}`
  | *glob*: `{}`
  | *dir*: `{}`







**output**::
    Lists of bidirectional best blasts

  | *type*: `map`
  | *source*: `input`
  | *category*: `output`
  | *optional*: `True`
  | *extension*: `{}`
  | *glob*: `{}`
  | *dir*: `{}`







**reference**::
    Reference fasta file to compare against

  | *type*: `map`
  | *source*: `{}`
  | *category*: `prerequisite`
  | *optional*: `False`
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



**eval**::
    e value cutoff

  | *type*: `float`
  | *default*: `1e-10`
  | *optional*: `True`



**nothreads**::
    Threads to run blast with with

  | *type*: `integer`
  | *default*: `4`
  | *optional*: `True`



**protein**::
    Is this a protein set

  | *type*: `boolean`
  | *default*: `F`
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
  Mark Fiers
**Creation date**
  Wed Nov 10 07:56:48 2010
**Modification date**
  1291933988.45



