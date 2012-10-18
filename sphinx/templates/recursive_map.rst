recursive_map
------------------------------------------------

**Recursively map a genome to the reference**


    Recursively map a resequence dataset against a reference genome



Commands
~~~~~~~~

**run**
  recusive map
  
  

Filesets
~~~~~~~~


**fq_forward**
  fastq input files directory - forward





**fq_reverse**
  fastq input files directory - reverse


  | *type*: `map`
  | *source*: `fq_forward`
  | *category*: `input`
  | *optional*: `True`
  | *pattern*: `*/*_2.fq`




**output**
  base output filename


  | *type*: `single`
  | *category*: `output`
  | *optional*: `True`
  | *pattern*: `output`




**reference**
  


  | *type*: `single`
  | *category*: `prerequisite`
  | *optional*: `False`
  | *pattern*: `*/*`





Parameters
~~~~~~~~~~



**iterations**
  no of iterations to run

  | *type*: `integer`
  | *default*: `3`
  | *optional*: `True`



**param_first**
  First set of parameters - get the low hanging fruit

  | *type*: `string`
  | *default*: `--fast`
  | *optional*: `True`



**param_second**
  Second set of parameters - more sensitive

  | *type*: `string`
  | *default*: `--very-sensitive`
  | *optional*: `True`



**threads**
  Number of threads to use

  | *type*: `integer`
  | *default*: `4`
  | *optional*: `True`



miscellaneous
~~~~~~~~~~~~~

**Backend**
  ruff
**Author**
  Mark Fiers
**Creation date**
  Fri, 08 Jun 2012 13:32:30 +1200
**Modification date**
  Fri, 08 Jun 2012 13:43:19 +1200
