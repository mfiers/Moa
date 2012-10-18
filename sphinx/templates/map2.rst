map2
------------------------------------------------

**Execute a "map2" ad-hoc analysis**


    Execute one command, on a number of input files.



Commands
~~~~~~~~

**run**
  *no help defined*
  
  

Filesets
~~~~~~~~


**input1**
  "map" input files set 1





**input2**
  "map" input files set 2


  | *type*: `map`
  | *source*: `input1`
  | *category*: `input`
  | *optional*: `False`
  | *pattern*: `*/*`




**output**
  "map" output files


  | *type*: `map`
  | *source*: `input1`
  | *category*: `output`
  | *optional*: `True`
  | *pattern*: `./*`





Parameters
~~~~~~~~~~



**process**
  The command to execute

  | *type*: `string`
  | *default*: `True`
  | *optional*: `False`



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
