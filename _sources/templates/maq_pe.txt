maq_pe
------------------------------------------------




    Generate alignments in SAM format given paired end reads using Maq.



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
  | *source*: `fq_forward_input`
  | *category*: `output`
  | *optional*: `{}`
  | *pattern*: `./*.bam`




**bfa_output**
  BFA Index name


  | *type*: `single`
  | *category*: `other`
  | *optional*: `{}`
  | *pattern*: `{}`




**bfq_forward_output**
  bfq files - forward files


  | *type*: `map`
  | *source*: `fq_forward_input`
  | *category*: `output`
  | *optional*: `{}`
  | *pattern*: `./*_1.bfq`




**bfq_reverse_output**
  bfq files - reverse files


  | *type*: `map`
  | *source*: `fq_forward_input`
  | *category*: `output`
  | *optional*: `{}`
  | *pattern*: `./*_2.bfq`




**fa_input**
  directory with reference fasta file name





**fq_forward_input**
  fastq input files directory - forward files





**fq_reverse_input**
  fastq input files directory - reverse files


  | *type*: `map`
  | *source*: `fq_forward_input`
  | *category*: `input`
  | *optional*: `{}`
  | *pattern*: `*/*_2.fq`




**map_output**
  maq map output files


  | *type*: `map`
  | *source*: `fq_forward_input`
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
  Any extra parameters

  | *type*: `string`
  | *default*: ``
  | *optional*: `True`



**first_read_len**
  length of the first read (<=127)s

  | *type*: `integer`
  | *default*: `0`
  | *optional*: `True`



**match_in_colorspace**
  match in the colorspace

  | *type*: `boolean`
  | *default*: `False`
  | *optional*: `True`



**max_dist_read_pairs**
  max distance between two paired reads s

  | *type*: `integer`
  | *default*: `250`
  | *optional*: `True`



**max_dist_RF_read_pairs**
  max distance between two RF paired reads s

  | *type*: `integer`
  | *default*: `0`
  | *optional*: `True`



**max_mismatch_qual_sum**
  maximum allowed sum of qualities of mismatches

  | *type*: `integer`
  | *default*: `70`
  | *optional*: `True`



**max_num_hits_out**
  max number of hits to output. >512 for all 01 hits.

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



**sec_read_len**
  length of the second read (<=127)s

  | *type*: `integer`
  | *default*: `0`
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
  Wed Dec 03 17:06:48 2010
**Modification date**
  unknown
