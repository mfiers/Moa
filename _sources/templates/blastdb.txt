blastdb
------------------------------------------------

 - 

Commands
~~~~~~~~

**clean**
  Remove all job data, not the Moa job itself, note that this must be implemented by the template.


**run**
  Takes either a set of fasta files or a single multi-fasta input file and creates a BLAST database.





Parameters
~~~~~~~~~~



**fasta_file** - The file with all input FASTA sequences for the blastdb.
  | *type*: `file`
  | *default*: `{}`
  | *optional*: `False`



**name** - Name of the BLAST database to create.
  | *type*: `string`
  | *default*: `blastdb`
  | *optional*: `True`



**protein** - Protein database? (T)rue) or not (F)alse (default: F)
  | *type*: `set`
  | *default*: `F`
  | *optional*: `True`



**title** - A name for this job
  | *type*: `string`
  | *default*: ``
  | *optional*: `False`



Other
~~~~~

**Backend**
  gnumake
**Author**
  Mark Fiers
**Creation date**
  Wed Nov 10 07:56:48 2010
**Modification date**
  Wed Nov 10 07:56:48 2010



