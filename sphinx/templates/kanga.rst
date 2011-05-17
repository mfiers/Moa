kanga
------------------------------------------------




    use kanga to align short reads to a reference genome



Commands
~~~~~~~~

**clean**
  Remove all job data, not the Moa job itself, note that this must be implemented by the template.
  
  
**run**
  run kanga
  
  

Filesets
~~~~~~~~


**input_fasta**
  Fasta input file





**output**
  output files


  | *type*: `map`
  | *source*: `rds_input`
  | *category*: `output`
  | *optional*: `True`
  | *pattern*: `./*.sam`




**output_bam**
  output files


  | *type*: `map`
  | *source*: `rds_input`
  | *category*: `output`
  | *optional*: `True`
  | *pattern*: `./*.bam`




**output_log**
  output log file


  | *type*: `map`
  | *source*: `rds_input`
  | *category*: `output`
  | *optional*: `{}`
  | *pattern*: `./*.log.txt`




**rds_input**
  rds (preprocessed) input files





**sfx_input**
  sfx array lookup file






Parameters
~~~~~~~~~~



**color_space**
  process for colorspace (SOLiD)

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



**max_Ns**
  maximum number of intermediate N's in reads before treating read as unalignable

  | *type*: `integer`
  | *default*: `1`
  | *optional*: `True`



**max_pair_len**
  accept paired end alignments with apparent length of at most this

  | *type*: `integer`
  | *default*: `300`
  | *optional*: `True`



**min_pair_len**
  accept paired end alignments with apparent length of at least this

  | *type*: `integer`
  | *default*: `100`
  | *optional*: `True`



**no_multireads**
  do not accept multiple reads aligning to the same loci

  | *type*: `boolean`
  | *default*: `False`
  | *optional*: `True`



**out_format**
  0 - CSV loci only, 1 - CSV loci + match sequence, 2 - CSV loci + read sequence, 3 - CSV loci + read + match sequence, 4 - UCSC BED, 5 - SAM format

  | *type*: `integer`
  | *default*: `0`
  | *optional*: `True`



**pe_mode**
  0 - none, 1 - paired ends with recover orphan ends, 2 - paired end no orphan recovery

  | *type*: `integer`
  | *default*: `0`
  | *optional*: `True`



**quality**
  fastq quality scoring- 0 - sanger, 1m - Illumina 1.3+, 2 - Solexa < 1.3, 3 - Ignore quality

  | *type*: `integer`
  | *default*: `3`
  | *optional*: `True`



**thread_num**
  number of processing threads (0 sets threads to number of CPU cores)

  | *type*: `integer`
  | *default*: `0`
  | *optional*: `True`



**trim3**
  trim this number of bases from 3' end of reads when loading raw reads

  | *type*: `integer`
  | *default*: `0`
  | *optional*: `True`



**trim5**
  trim this number of bases from 5' end of reads when loading raw reads

  | *type*: `integer`
  | *default*: `0`
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
