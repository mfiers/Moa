soapdenovo_postprocess
------------------------------------------------




    Run Soapdenovo



Commands
~~~~~~~~

**run**
  Postprocess - run GapCloser & SSpace
  
  

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




**input**
  input scaffold to process


  | *type*: `single`
  | *category*: `input`
  | *optional*: `False`
  | *pattern*: `{}`




**output**
  output file to generate


  | *type*: `single`
  | *category*: `output`
  | *optional*: `True`
  | *pattern*: `final.fasta`





Parameters
~~~~~~~~~~



**avg_insert**
  library insert size

  | *type*: `integer`
  | *default*: `200`
  | *optional*: `{}`



**noruns**
  no times to run gapcloser & SSPace

  | *type*: `integer`
  | *default*: `2`
  | *optional*: `True`



**run_sspace**
  run SSPace? use

  | *type*: `boolean`
  | *default*: `True`
  | *optional*: `True`



**sspace_executable**
  SSPace executable

  | *type*: `{}`
  | *default*: `SSPACE_Basic_v2.0.pl`
  | *optional*: `True`



**sspace_extra_variables**
  Extra variables to pass to Sspace

  | *type*: `{}`
  | *default*: ``
  | *optional*: `True`



**threads**
  no threads to use

  | *type*: `integer`
  | *default*: `8`
  | *optional*: `True`



miscellaneous
~~~~~~~~~~~~~

**Backend**
  ruff
**Author**
  Mark Fiers
**Creation date**
  Mon, 21 Nov 2011 12:47:16
**Modification date**
  Mon, 21 Nov 2011 12:47:22
