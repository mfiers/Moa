samtools_pileup
------------------------------------------------




    Print the alignment in the pileup format.



Commands
~~~~~~~~

**clean**
  Remove all job data, not the Moa job itself
  
  
**run**
  run samtools pileup command
  
  

Filesets
~~~~~~~~


**fasta**
  reference fasta file


  | *type*: `single`
  | *category*: `prerequisite`
  | *optional*: `True`
  | *pattern*: `*/*.fasta`




**input**
  bam or sam files





**output**
  


  | *type*: `map`
  | *source*: `input`
  | *category*: `output`
  | *optional*: `{}`
  | *pattern*: `./*.pileup`




**output_bam**
  


  | *type*: `map`
  | *source*: `input`
  | *category*: `output`
  | *optional*: `{}`
  | *pattern*: `./*.sorted`





Parameters
~~~~~~~~~~



**cap_mapQ_at**
  cap mapping quality at INT

  | *type*: `integer`
  | *default*: `60`
  | *optional*: `True`



**extra_params**
  any extra parameters

  | *type*: `string`
  | *default*: ``
  | *optional*: `True`



**filter_read_bits**
  filtering reads with bits in INT

  | *type*: `integer`
  | *default*: `1796`
  | *optional*: `True`



**input_is_SAM**
  the input is in SAM

  | *type*: `boolean`
  | *default*: `False`
  | *optional*: `True`



**num_haplotypes**
  number of haplotypes in the sample (for -c/-g)

  | *type*: `integer`
  | *default*: `2`
  | *optional*: `True`



**out_2nd_best**
  output the 2nd best call and quality

  | *type*: `boolean`
  | *default*: `False`
  | *optional*: `True`



**out_GLFv3_format**
  output in the GLFv3 format (suppressing -c/-i/-s)

  | *type*: `boolean`
  | *default*: `False`
  | *optional*: `True`



**out_maq_consensus**
  output the maq consensus sequence

  | *type*: `boolean`
  | *default*: `False`
  | *optional*: `True`



**phred_prob_indel**
  phred prob. of an indel in sequencing/prep. (for -c/-g)

  | *type*: `integer`
  | *default*: `40`
  | *optional*: `True`



**print_variants_only**
  print variants only (for -c)

  | *type*: `boolean`
  | *default*: `False`
  | *optional*: `True`



**prior_diff_haplotypes**
  phred prob. of an indel in sequencing/prep. (for -c/-g)

  | *type*: `float`
  | *default*: `0.001`
  | *optional*: `True`



**prior_indel_haplotypes**
  number of haplotypes in the sample (for -c/-g)

  | *type*: `float`
  | *default*: `0.00015`
  | *optional*: `True`



**show_lines_indels**
  only show lines/consensus with indels

  | *type*: `boolean`
  | *default*: `False`
  | *optional*: `True`



**simple_pileup_format**
  simple (yet incomplete) pileup format

  | *type*: `boolean`
  | *default*: `False`
  | *optional*: `True`



**theta_maq_model**
  number of haplotypes in the sample (for -c/-g)

  | *type*: `float`
  | *default*: `0.85`
  | *optional*: `True`



**use_SOAPsnp_model**
  use the SOAPsnp model for SNP calling

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
  Wed Dec 15 17:06:48 2010
**Modification date**
  unknown
