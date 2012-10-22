bowtiedb
------------------------------------------------




    Builds a bowtie index from a reference sequence



Commands
~~~~~~~~

**clean**
  Remove all job data, not the Moa job itself, note that this must be implemented by the template.
  
  
**run**
  Create the bowtie database
  
  

Filesets
~~~~~~~~


**input**
  Input fasta file for the bowtie database





**output**
  database name to create


  | *type*: `single`
  | *category*: `output`
  | *optional*: `{}`
  | *pattern*: `db`





Parameters
~~~~~~~~~~



**extra_params**
  any option parameters

  | *type*: `string`
  | *default*: ``
  | *optional*: `True`



**title**
  

  | *type*: `{}`
  | *default*: `Bowtie index builder`
  | *optional*: `{}`



miscellaneous
~~~~~~~~~~~~~

**Backend**
  ruff
**Author**
  Mark Fiers
**Creation date**
  Wed Nov 10 07:56:48 2010
**Modification date**
  Wed Dec 09 07:56:48 2010
