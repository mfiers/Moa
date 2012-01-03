bdbb
------------------------------------------------

**Bidirectional best BLAST hit**


    Discover the bidirectional best blast hit between two sets of sequences



Commands
~~~~~~~~

**clean**
  Remove all job data, not the Moa job itself, note that this must be implemented by the template.
  
  
**run**
  generate a list of bidirectional best blast hits between two databases of sequences
  
  

Filesets
~~~~~~~~


**input_a**
  First multi fasta input set


  | *type*: `single`
  | *category*: `input`
  | *optional*: `False`
  | *pattern*: `*/*.fasta`




**input_b**
  Second multi fasta input set


  | *type*: `single`
  | *category*: `input`
  | *optional*: `False`
  | *pattern*: `*/*.fasta`




**output**
  List of bidirectional best blasts hits


  | *type*: `map`
  | *source*: `input_a`
  | *category*: `output`
  | *optional*: `True`
  | *pattern*: `*/*.list`





Parameters
~~~~~~~~~~



**eval**
  e value cutoff

  | *type*: `float`
  | *default*: `1e-10`
  | *optional*: `True`



**extract**
  Extract the identified sequences from the input fasta files

  | *type*: `boolean`
  | *default*: `False`
  | *optional*: `True`



**nothreads**
  Threads to run blast with with

  | *type*: `integer`
  | *default*: `4`
  | *optional*: `True`



**protein**
  Is this a protein set

  | *type*: `boolean`
  | *default*: `False`
  | *optional*: `True`



**tblastx**
  If this is a nucleotide set, use tblastx?? (otherwise use blastn)

  | *type*: `boolean`
  | *default*: `F`
  | *optional*: `True`



miscellaneous
~~~~~~~~~~~~~

**Backend**
  ruff
**Author**
  Mark Fiers
**Creation date**
  Wed Nov 10 07:56:48 2010
**Modification date**
  unknown
