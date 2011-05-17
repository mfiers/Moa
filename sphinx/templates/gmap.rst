gmap
------------------------------------------------

**Gmap**


    Run GMAP on an set of input files (query) vs a database index.



Commands
~~~~~~~~

**clean**
  Remove all job data, not the Moa job itself, note that this must be implemented by the template.
  
  
**run**
  *no help defined*
  
  

Filesets
~~~~~~~~


**align**
  


  | *type*: `map`
  | *source*: `input`
  | *category*: `output`
  | *optional*: `{}`
  | *pattern*: `./align/*.align`




**genepred**
  


  | *type*: `map`
  | *source*: `input`
  | *category*: `output`
  | *optional*: `{}`
  | *pattern*: `./genepred/*.genepred`




**gff**
  


  | *type*: `map`
  | *source*: `input`
  | *category*: `output`
  | *optional*: `{}`
  | *pattern*: `./gff/*.gff`




**gff_invert**
  


  | *type*: `map`
  | *source*: `input`
  | *category*: `output`
  | *optional*: `{}`
  | *pattern*: `./gff/*.invert.gff`




**input**
  Sequences to map





**raw**
  


  | *type*: `map`
  | *source*: `input`
  | *category*: `output`
  | *optional*: `{}`
  | *pattern*: `./raw/*.raw`





Parameters
~~~~~~~~~~



**db**
  Gmap db

  | *type*: `file`
  | *default*: ``
  | *optional*: `False`



**extra_parameters**
  extra parameters to feed to gmap

  | *type*: `string`
  | *default*: ``
  | *optional*: `True`



**gff_source**
  Source field to use in the output GFF

  | *type*: `string`
  | *default*: `gmap`
  | *optional*: `True`



**invert_gff**
  Invert the GFF (T/*F*)

  | *type*: `set`
  | *default*: `T`
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
