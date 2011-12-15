abyss_pe
------------------------------------------------




    Run Abysspe



Commands
~~~~~~~~

**clean**
  Remove all job data
  
  
**run**
  Execute abysspe in paired-end mode
  
  

Filesets
~~~~~~~~


**fq_forward**
  fastq input files directory - forward





**fq_reverse**
  fastq input files directory - reverse


  | *type*: `map`
  | *source*: `fq_forward`
  | *category*: `input`
  | *optional*: `True`
  | *pattern*: `*/*_2.fq`




**output**
  soap denovo output file


  | *type*: `single`
  | *category*: `output`
  | *optional*: `True`
  | *pattern*: `{}`





Parameters
~~~~~~~~~~



**joinpairs**
  number of pairs needed to consider joining two contigs

  | *type*: `integer`
  | *default*: `10`
  | *optional*: `True`



**kmer**
  kmer size

  | *type*: `integer`
  | *default*: `31`
  | *optional*: `True`



**threads**
  no threads to use

  | *type*: `integer`
  | *default*: `3`
  | *optional*: `True`



miscellaneous
~~~~~~~~~~~~~

**Backend**
  ruff
**Author**
  Mark Fiers
**Creation date**
  Mon, 21 Nov 2011 12:47:16
**Modification date**
  Mon, 21 Nov 2011 12:47:22
