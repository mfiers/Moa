bfast_db
------------------------------------------------




    Generate db index files for aligning reads with bfast



Commands
~~~~~~~~

**clean**
  Remove all job data, not the Moa job itself
  
  
**run**
  run bfast fasta2brg and index commands
  
  

Filesets
~~~~~~~~


**fa_input**
  fasta input file






Parameters
~~~~~~~~~~



**algorithm_colour_space**
  true -> colour space, false -> NT space

  | *type*: `boolean`
  | *default*: `False`
  | *optional*: `True`



**depth**
  The depth of the splitting(d). The index will be split into 4^d parts.

  | *type*: `integer`
  | *default*: `0`
  | *optional*: `True`



**extra_params**
  Any extra parameters

  | *type*: `string`
  | *default*: ``
  | *optional*: `True`



**hash_width**
  The hash width for the index (recommended from manual = 14)

  | *type*: `integer`
  | *default*: `{}`
  | *optional*: `False`



**index_num**
  Specifies this is the ith index you are creating

  | *type*: `integer`
  | *default*: `1`
  | *optional*: `True`



**mask**
  The mask or spaced seed to use.

  | *type*: `string`
  | *default*: `{}`
  | *optional*: `False`



**print_params**
  print program parameters

  | *type*: `boolean`
  | *default*: `False`
  | *optional*: `True`



**thread_num**
  Specifies the number of threads to use

  | *type*: `integer`
  | *default*: `1`
  | *optional*: `True`



**timing_information**
  specifies output timing information

  | *type*: `boolean`
  | *default*: `True`
  | *optional*: `True`



**usage_summary**
  Display usage summary (help)

  | *type*: `boolean`
  | *default*: `False`
  | *optional*: `True`



miscellaneous
~~~~~~~~~~~~~

**Backend**
  ruff
**Author**
  Yogini Idnani, Mark Fiers
**Creation date**
  Wed Feb 15 10:06:48 2011
**Modification date**
  unknown
