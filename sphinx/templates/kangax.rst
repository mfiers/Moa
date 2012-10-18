kangax
------------------------------------------------




    use kangax to create the suffix array lookup database for the reference genome



Commands
~~~~~~~~

**clean**
  Remove all job data, not the Moa job itself, note that this must be implemented by the template.
  
  
**run**
  run kangax
  
  

Filesets
~~~~~~~~


**input_fasta**
  Fasta input file





**output_log**
  output log file


  | *type*: `map`
  | *source*: `input_fasta`
  | *category*: `output`
  | *optional*: `{}`
  | *pattern*: `./*.log.txt`




**output_sfx**
  output suffix array lookup


  | *type*: `map`
  | *source*: `input_fasta`
  | *category*: `output`
  | *optional*: `{}`
  | *pattern*: `./*.sfx`





Parameters
~~~~~~~~~~



**block_seq_len**
  generated suffix blocks to hold at most this length (MB) concatenated sequences

  | *type*: `integer`
  | *default*: `3300`
  | *optional*: `True`



**color_space**
  generate for colorspace (SOLiD)

  | *type*: `boolean`
  | *default*: `False`
  | *optional*: `True`



**extra_params**
  any extra parameters

  | *type*: `string`
  | *default*: ``
  | *optional*: `True`



**help**
  print this help and exit

  | *type*: `boolean`
  | *default*: `False`
  | *optional*: `True`



**reference_species**
  reference species

  | *type*: `string`
  | *default*: ``
  | *optional*: `False`



**target_dep**
  generate target file only if missing or older than any independent source files

  | *type*: `boolean`
  | *default*: `False`
  | *optional*: `True`



**version**
  print version information and exit

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
  Wed Nov 10 07:56:48 2010
**Modification date**
  unknown
