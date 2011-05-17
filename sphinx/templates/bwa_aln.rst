bwa_aln
------------------------------------------------




    Use BWA to align a set of fastq reads against a db



Commands
~~~~~~~~

**clean**
  Remove all job data, not the Moa job itself, note that this must be implemented by the template.
  
  
**run**
  run bwa aln
  
  

Filesets
~~~~~~~~


**input**
  Fastq input files





**output**
  


  | *type*: `map`
  | *source*: `input`
  | *category*: `output`
  | *optional*: `{}`
  | *pattern*: `./*.sai`





Parameters
~~~~~~~~~~



**best_hits_stop**
  stop searching when there are >INT equally best hits

  | *type*: `integer`
  | *default*: `30`
  | *optional*: `True`



**color_space**
  input sequences are in the color space

  | *type*: `boolean`
  | *default*: `False`
  | *optional*: `True`



**db**
  bwa database to align against

  | *type*: `string`
  | *default*: ``
  | *optional*: `False`



**edit_dist_missing_prob**
  max

  | *type*: `integer`
  | *default*: `0.04`
  | *optional*: `True`



**gap_ext_max**
  maximum number of gap extensions, -1 for disabling long gaps

  | *type*: `integer`
  | *default*: `-1`
  | *optional*: `True`



**gap_ext_penalty**
  gap extension penalty

  | *type*: `integer`
  | *default*: `4`
  | *optional*: `True`



**gap_open_penalty**
  gap open penalty

  | *type*: `integer`
  | *default*: `11`
  | *optional*: `True`



**gap_opens_max**
  maximum number or fraction of gap opens

  | *type*: `integer`
  | *default*: `1`
  | *optional*: `True`



**log_gap_penalty_del**
  log-scaled gap penalty for long deletions

  | *type*: `boolean`
  | *default*: `False`
  | *optional*: `True`



**max_ext_long_del**
  maximum occurrences for extending a long deletion

  | *type*: `integer`
  | *default*: `10`
  | *optional*: `True`



**max_queue_entry**
  maximum entries in the queue

  | *type*: `integer`
  | *default*: `2000000`
  | *optional*: `True`



**mismatch_penalty**
  mismatch penalty

  | *type*: `integer`
  | *default*: `3`
  | *optional*: `True`



**no_indel_from_ends**
  do not put an indel within INT bp towards the ends

  | *type*: `integer`
  | *default*: `5`
  | *optional*: `True`



**non_iterative**
  non-iterative mode search for all n-difference hits (slow)

  | *type*: `boolean`
  | *default*: `False`
  | *optional*: `True`



**quality_step**
  quality threshold for read trimming down to 35bp

  | *type*: `integer`
  | *default*: `0`
  | *optional*: `True`



**seed_len**
  Seed length

  | *type*: `integer`
  | *default*: `30`
  | *optional*: `True`



**seed_max_diff**
  Maximum differences in the seed

  | *type*: `integer`
  | *default*: `2`
  | *optional*: `True`



**thread_num**
  number of threads

  | *type*: `integer`
  | *default*: `1`
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
