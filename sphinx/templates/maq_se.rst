maq_se
------------------------------------------------




    Generate alignments in SAM format given single end reads using Maq.



Commands
~~~~~~~~

**clean**
  Remove all job data, not the Moa job itself
  
  
**run**
  run maq's fasta2bfa, fastq2bfq and map.
  
  

Filesets
~~~~~~~~


**bam_output**
  bam alignment output file


  | *type*: `map`
  | *source*: `fq_input`
  | *category*: `output`
  | *optional*: `{}`
  | *pattern*: `./*.bam`




**bfa_output**
  BFA Index name


  | *type*: `single`
  | *category*: `other`
  | *optional*: `{}`
  | *pattern*: `{}`




**bfq_output**
  bfq files - forward files


  | *type*: `map`
  | *source*: `fq_input`
  | *category*: `output`
  | *optional*: `{}`
  | *pattern*: `./*.bfq`




**fa_input**
  directory with reference fasta file name





**fq_input**
  fastq input files





**map_output**
  maq map output files


  | *type*: `map`
  | *source*: `fq_input`
  | *category*: `output`
  | *optional*: `{}`
  | *pattern*: `./*.map`





Parameters
~~~~~~~~~~



**disable_sw**
  disable Smith-Waterman alignment

  | *type*: `boolean`
  | *default*: `False`
  | *optional*: `True`



**extra_parameters**
  other parameters

  | *type*: `string`
  | *default*: ``
  | *optional*: `True`



**match_in_colorspace**
  match in the colorspace

  | *type*: `boolean`
  | *default*: `False`
  | *optional*: `True`



**max_mismatch_qual_sum**
  maximum allowed sum of qualities of mismatches

  | *type*: `integer`
  | *default*: `70`
  | *optional*: `True`



**max_num_hits_out**
  number of mismatches in the first 24bp

  | *type*: `integer`
  | *default*: `250`
  | *optional*: `True`



**num_mismatch_24bp**
  number of mismatches in the first 24bp

  | *type*: `integer`
  | *default*: `2`
  | *optional*: `True`



**read_ref_diff_rate**
  rate of difference between reads and references

  | *type*: `float`
  | *default*: `0.001`
  | *optional*: `True`



**trim_all_reads**
  trim all reads (usually not recommended)

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
  Wed Dec 02 17:06:48 2010
**Modification date**
  unknown
