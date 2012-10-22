smalt_pe
------------------------------------------------




    Run SMALT on an set of input files (query) vs a database index.



Commands
~~~~~~~~

**clean**
  Remove all job data, not the Moa job itself
  
  
**run**
  Execute SMALT with with paired-end fastq
  
  

Filesets
~~~~~~~~


**db**
  The (basename of the) smalt database to use.


  | *type*: `single`
  | *category*: `prerequisite`
  | *optional*: `False`
  | *pattern*: `../10.smaltdb/db`




**fasta**
  reference fasta file


  | *type*: `single`
  | *category*: `prerequisite`
  | *optional*: `False`
  | *pattern*: `*.fasta`




**fq_forward_input**
  fastq input files directory - forward





**fq_reverse_input**
  fastq input files directory - reverse


  | *type*: `map`
  | *source*: `fq_forward_input`
  | *category*: `input`
  | *optional*: `True`
  | *pattern*: `*/*_2.fq`




**output**
  output BAM file (automatically converted & filtered for reads that to not map)


  | *type*: `map`
  | *source*: `fq_forward_input`
  | *category*: `output`
  | *optional*: `{}`
  | *pattern*: `./*.sam`





Parameters
~~~~~~~~~~



**extra_params**
  extra parameters to feed to smalt

  | *type*: `string`
  | *default*: ``
  | *optional*: `True`



**max_insertsize**
  Maximum allowed insertsize

  | *type*: `integer`
  | *default*: `250`
  | *optional*: `True`



**min_insertsize**
  Minimum allowed insertsize

  | *type*: `integer`
  | *default*: `1`
  | *optional*: `True`



**output_format**
  output format (sam or samsoft)

  | *type*: `{}`
  | *default*: `sam`
  | *optional*: `True`



**pairtype**
  pair type (pe: fr/illumina short; mp: rf/illumina mate pairs or pp: ff

  | *type*: `{}`
  | *default*: `pe`
  | *optional*: `True`



**threads**
  No threads to use

  | *type*: `int`
  | *default*: `4`
  | *optional*: `True`



miscellaneous
~~~~~~~~~~~~~

**Backend**
  ruff
**Author**
  Mark Fiers
**Creation date**
  Tue, 27 Mar 2012 10:05:40 +1300
**Modification date**
  Tue, 27 Mar 2012 10:31:09 +1300
