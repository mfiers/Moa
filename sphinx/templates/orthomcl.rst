orthomcl
------------------------------------------------

**Bwa index builder**


    Run orhthomcl on a set of input fasta files



Commands
~~~~~~~~

**clean**
  Remove all job data
  
  
**run**
  Run orthomcl
  
  
  **run** delegates execution to: **prep_1**
  

Filesets
~~~~~~~~


**input**
  Directory with the input fasta files






Parameters
~~~~~~~~~~



**db**
  DB name

  | *type*: `string`
  | *default*: `orthomcl`
  | *optional*: `True`



**host**
  DB host

  | *type*: `string`
  | *default*: `localhost`
  | *optional*: `True`



**login**
  DB login

  | *type*: `string`
  | *default*: `{}`
  | *optional*: `False`



**pass**
  DB password

  | *type*: `string`
  | *default*: `{}`
  | *optional*: `False`



**port**
  DB port

  | *type*: `string`
  | *default*: `3306`
  | *optional*: `True`



**prefix**
  prefix for separating tables & output fields

  | *type*: `string`
  | *default*: `run1`
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
