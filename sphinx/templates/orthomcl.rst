orthomcl
------------------------------------------------

**Bwa index builder**

::
    Run orhthomcl on a set of input fasta files


Commands
~~~~~~~~

**clean**
  Remove all job data


**run**
  Run orthomcl





Filesets
~~~~~~~~




**input**::
    Directory with the input fasta files

  | *type*: `map`
  | *source*: `{}`
  | *category*: `input`
  | *optional*: `False`
  | *extension*: `{}`
  | *glob*: `{}`
  | *dir*: `{}`






Parameters
~~~~~~~~~~



**db**::
    DB name

  | *type*: `string`
  | *default*: `orthomcl`
  | *optional*: `True`



**default_command**::
    command to run for this template

  | *type*: `{}`
  | *default*: `run`
  | *optional*: `True`



**host**::
    DB host

  | *type*: `string`
  | *default*: `localhost`
  | *optional*: `True`



**login**::
    DB login

  | *type*: `string`
  | *default*: `{}`
  | *optional*: `False`



**pass**::
    DB password

  | *type*: `string`
  | *default*: `{}`
  | *optional*: `False`



**port**::
    DB port

  | *type*: `string`
  | *default*: `3306`
  | *optional*: `True`



**prefix**::
    prefix for separating tables & output fields

  | *type*: `string`
  | *default*: `run1`
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
  Wed Nov 10 07:56:48 2010



