fastainfo
------------------------------------------------

**gather information on a set of fasta files**


    gather info on a set of input files



Commands
~~~~~~~~

**finish**
  create a report
  
  
**run**
  generate info on each of the input sequences
  
  

Filesets
~~~~~~~~


**input**
  "fastainfo" input files





**output**
  "fastainfo" raw output files


  | *type*: `map`
  | *source*: `input`
  | *category*: `output`
  | *optional*: `True`
  | *pattern*: `stats/*.out`




**stats**
  "fastainfo" collect stat files


  | *type*: `map`
  | *source*: `input`
  | *category*: `output`
  | *optional*: `True`
  | *pattern*: `stats/*.stat`





Parameters
~~~~~~~~~~



miscellaneous
~~~~~~~~~~~~~

**Backend**
  ruff
**Author**
  Mark Fiers
**Creation date**
  Mon, 11 Jul 2011 15:15:20
**Modification date**
  Mon, 11 Jul 2011 15:15:12
