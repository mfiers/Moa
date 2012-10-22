gmapdb
------------------------------------------------

**gmapdb index builder**


    Builds gmapdb index from a reference sequence



Commands
~~~~~~~~

**clean**
  Remove all job data, not the Moa job itself, note that this must be implemented by the template.
  
  
**run**
  *no help defined*
  
  

Filesets
~~~~~~~~


**input**
  The reference sequence to build a gmap database with.


  | *type*: `single`
  | *category*: `input`
  | *optional*: `False`
  | *pattern*: `*/*.fasta`





Parameters
~~~~~~~~~~



**name**
  Name of the gmap index to create

  | *type*: `string`
  | *default*: `gmapdb`
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
  Wed Nov 10 07:56:48 2010
