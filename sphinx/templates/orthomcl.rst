orthomcl
------------------------------------------------

**Run OrthoMCL**


    Execute one command, No in or output files are tracked by Moa.



Commands
~~~~~~~~

**run**
  *no help defined*
  
  

Parameters
~~~~~~~~~~



**db**
  Db name

  | *type*: `string`
  | *default*: `{}`
  | *optional*: `False`



**eval**
  Evalue cutoff for blast to use

  | *type*: `string`
  | *default*: `1e-5`
  | *optional*: `True`



**group_prefix**
  OrthoMCL prefix for group names

  | *type*: `string`
  | *default*: `g_`
  | *optional*: `True`



**host**
  Db Host

  | *type*: `localhost`
  | *default*: `{}`
  | *optional*: `True`



**input_dir**
  Input directory with compliant (read the manual) fasta files

  | *type*: `string`
  | *default*: `{}`
  | *optional*: `False`



**login**
  Db username

  | *type*: `string`
  | *default*: `None`
  | *optional*: `False`



**mcl_i**
  mcl -i value

  | *type*: `float`
  | *default*: `1.5`
  | *optional*: `True`



**num_threads**
  Number of threads to use

  | *type*: `integer`
  | *default*: `4`
  | *optional*: `True`



**pass**
  Db password

  | *type*: `string`
  | *default*: `None`
  | *optional*: `False`



**port**
  Db port

  | *type*: `integer`
  | *default*: `3306`
  | *optional*: `True`



**prefix**
  OrthoMCL prefix for the database tables

  | *type*: `string`
  | *default*: `ortho`
  | *optional*: `True`



**vendor**
  Db vendor

  | *type*: `string`
  | *default*: `mysql`
  | *optional*: `True`



miscellaneous
~~~~~~~~~~~~~

**Backend**
  ruff
**Author**
  Mark Fiers
**Creation date**
  Tue Mar 29 16:34:19 2011
**Modification date**
  Wed Mar 30 06:02:01 2011
