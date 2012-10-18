smaltdb
------------------------------------------------

**Smalt index builder**


    Builds a smalt index from a reference sequence



Commands
~~~~~~~~

**clean**
  Remove all job data, not the Moa job itself, note that this must be implemented by the template.
  
  
**run**
  Create the smalt index
  
  

Filesets
~~~~~~~~


**input**
  Input fasta file for the smalt database


  | *type*: `single`
  | *category*: `input`
  | *optional*: `False`
  | *pattern*: `*/*.fasta`




**output**
  database name to create


  | *type*: `single`
  | *category*: `output`
  | *optional*: `{}`
  | *pattern*: `db`





Parameters
~~~~~~~~~~



**word_length**
  word length

  | *type*: `int`
  | *default*: `10`
  | *optional*: `True`



**word_spacing**
  word spacing

  | *type*: `int`
  | *default*: `6`
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
  Wed Dec 09 07:56:48 2010
