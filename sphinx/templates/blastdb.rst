blastdb
------------------------------------------------




Commands
~~~~~~~~

**clean**
  Remove all job data, not the Moa job itself, note that this must be implemented by the template.
  
  
**run**
  Takes either a set of fasta files or a single multi-fasta input file and creates a BLAST database.
  
  

Filesets
~~~~~~~~


**dbname**
  


  | *type*: `map`
  | *source*: `input`
  | *category*: `output`
  | *optional*: `{}`
  | *pattern*: `./db`




**input**
  The file with all input FASTA sequences for the blastdb.


  | *type*: `single`
  | *category*: `input`
  | *optional*: `False`
  | *pattern*: `*/*.fasta`





Parameters
~~~~~~~~~~



**protein**
  Protein database? (T)rue) or not (F)alse (default: F)

  | *type*: `set`
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
  Tue, 03 Jan 2012 15:00:23
