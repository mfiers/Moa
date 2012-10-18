bfast_aln
------------------------------------------------




    Generate bam format alignments using bfast



Commands
~~~~~~~~

**clean**
  Remove all job data, not the Moa job itself
  
  
**run**
  run bfast match, localalign, postprocess commands
  
  

Filesets
~~~~~~~~


**fa_input**
  fasta input file





**fq_input**
  fastq input files





**output_aln**
  


  | *type*: `map`
  | *source*: `fq_input`
  | *category*: `output`
  | *optional*: `{}`
  | *pattern*: `./*.aln`




**output_bam**
  


  | *type*: `map`
  | *source*: `fq_input`
  | *category*: `output`
  | *optional*: `{}`
  | *pattern*: `./*.bam`





Parameters
~~~~~~~~~~



**algorithm_colour_space**
  true -> colour space, false -> NT space

  | *type*: `boolean`
  | *default*: `False`
  | *optional*: `True`



**avg_mism_qual**
  Specifies the average mismatch quality

  | *type*: `integer`
  | *default*: `10`
  | *optional*: `True`



**extra_params_localalign**
  Any extra parameters for the localalign command

  | *type*: `string`
  | *default*: ``
  | *optional*: `True`



**extra_params_match**
  Any extra parameters for the match command

  | *type*: `string`
  | *default*: ``
  | *optional*: `True`



**extra_params_postprocess**
  Any extra parameters for the postprocess command

  | *type*: `string`
  | *default*: ``
  | *optional*: `True`



**min_mapping_qual**
  Specifies to remove low mapping quality alignments

  | *type*: `integer`
  | *default*: `-2147483648`
  | *optional*: `True`



**min_norm_score**
  Specifies to remove low (alignment) scoring alignments

  | *type*: `integer`
  | *default*: `-2147483648`
  | *optional*: `True`



**output_format**
  0 - BAF, 1 - SAM

  | *type*: `integer`
  | *default*: `1`
  | *optional*: `True`



**paired_opp_strands**
  Specifies that paired reads are on opposite strands

  | *type*: `boolean`
  | *default*: `False`
  | *optional*: `True`



**pairing_std_dev**
  Specifies the pairing distance standard deviation to examine when recuing

  | *type*: `float`
  | *default*: `2.0`
  | *optional*: `True`



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



**ungapped_aln**
  Do ungapped local alignment

  | *type*: `boolean`
  | *default*: `False`
  | *optional*: `True`



**ungapped_pairing_rescue**
  Specifies that ungapped pairing rescue should be performed

  | *type*: `boolean`
  | *default*: `False`
  | *optional*: `True`



**unpaired_reads**
  True value specifies that pairing should not be performed

  | *type*: `boolean`
  | *default*: `False`
  | *optional*: `True`



**usage_summary**
  Display usage summary (help)

  | *type*: `boolean`
  | *default*: `False`
  | *optional*: `True`



**which_strand**
  0 - consider both strands, 1 - forwards strand only, 2 - reverse strand only

  | *type*: `integer`
  | *default*: `0`
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
