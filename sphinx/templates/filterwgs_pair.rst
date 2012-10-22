filterwgs_pair
------------------------------------------------

**Execute a "map22" ad-hoc analysis - two input files, two output files**


    Filter raw WGS data



Commands
~~~~~~~~

**run**
  Filter WGS data
  
  

Filesets
~~~~~~~~


**input1**
  forward input fastq





**input2**
  reverse input fastq


  | *type*: `map`
  | *source*: `input1`
  | *category*: `input`
  | *optional*: `False`
  | *pattern*: `*/*`




**output1**
  forward output fastq


  | *type*: `map`
  | *source*: `input1`
  | *category*: `output`
  | *optional*: `True`
  | *pattern*: `./*`




**output2**
  reverse output fastq


  | *type*: `map`
  | *source*: `input1`
  | *category*: `output`
  | *optional*: `True`
  | *pattern*: `./*`





Parameters
~~~~~~~~~~



**adapters**
  Fasta file with the adapter sequences to trim

  | *type*: `file`
  | *default*: `{}`
  | *optional*: `False`



**minlen**
  Minimum remaining sequence length

  | *type*: `int`
  | *default*: `50`
  | *optional*: `True`



**qual**
  quality threshold causing trimming

  | *type*: `int`
  | *default*: `13`
  | *optional*: `True`



**title**
  

  | *type*: `{}`
  | *default*: `Filter paired fastq files using fastq-mcf`
  | *optional*: `{}`



miscellaneous
~~~~~~~~~~~~~

**Backend**
  ruff
**Author**
  Mark Fiers
**Creation date**
  Tue Mar 29 16:34:19 2011
**Modification date**
  Mon, 13 Feb 2012 09:16:36 +1300
