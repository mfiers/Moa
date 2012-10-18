fastx_clipper
------------------------------------------------




    run fastx_clipper



Commands
~~~~~~~~

**clean**
  Remove all job data, not the Moa job itself
  
  
**run**
  run fastx_clipper
  
  

Filesets
~~~~~~~~


**input**
  fastq input files directory





**output**
  


  | *type*: `map`
  | *source*: `input`
  | *category*: `output`
  | *optional*: `{}`
  | *pattern*: `./*.fq`





Parameters
~~~~~~~~~~



**adaptor**
  ADAPTER string. default is CCTTAAGG (dummy adapter).

  | *type*: `string`
  | *default*: `CCTTAAGG`
  | *optional*: `True`



**adaptor_and_bases**
  Keep the adapter and N bases after it.

  | *type*: `integer`
  | *default*: `0`
  | *optional*: `True`



**compress_output**
  Compress output with GZIP.

  | *type*: `boolean`
  | *default*: `False`
  | *optional*: `True`



**debug_output**
  DEBUG output.

  | *type*: `boolean`
  | *default*: `False`
  | *optional*: `True`



**help**
  help screen

  | *type*: `boolean`
  | *default*: `False`
  | *optional*: `True`



**keep_unknown_nuc_seq**
  keep sequences with unknown (N) nucleotides. default is to discard such sequences.

  | *type*: `boolean`
  | *default*: `False`
  | *optional*: `True`



**out_adaptor_only_seq**
  Report Adapter-Only sequences.

  | *type*: `boolean`
  | *default*: `False`
  | *optional*: `True`



**rm_clipped_seq**
  Discard clipped sequences (i.e. - keep only sequences which did not contained the adapter).

  | *type*: `boolean`
  | *default*: `False`
  | *optional*: `True`



**rm_non_clipped_seq**
  Discard non-clipped sequences (i.e. - keep only sequences which contained the adapter).

  | *type*: `boolean`
  | *default*: `False`
  | *optional*: `True`



**rm_short_seq**
  discard sequences shorter than N nucleotides. default is 5.

  | *type*: `integer`
  | *default*: `5`
  | *optional*: `True`



**verbose**
  Verbose - report number of sequences. If [-o] is specified,  report will be printed to STDOUT. If [-o] is not specified (and output goes to STDOUT), report will be printed to STDERR.

  | *type*: `boolean`
  | *default*: `False`
  | *optional*: `True`



miscellaneous
~~~~~~~~~~~~~

**Backend**
  ruff
**Author**
  Mark Fiers, Yogini Idnani
**Creation date**
  Wed Dec 06 17:06:48 2010
**Modification date**
  unknown
