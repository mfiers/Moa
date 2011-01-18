gmap
------------------------------------------------

**Gmap**

::
    Run GMAP on an set of input files (query) vs a database index.


Commands
~~~~~~~~

**clean**
  Remove all job data, not the Moa job itself, note that this must be implemented by the template.


**run**
  *no help defined*





Filesets
~~~~~~~~




**genepred**::
    {}

  | *type*: `map`
  | *source*: `input`
  | *category*: `output`
  | *optional*: `{}`
  | *extension*: `{}`
  | *glob*: `{}`
  | *dir*: `{}`







**gff**::
    {}

  | *type*: `map`
  | *source*: `input`
  | *category*: `output`
  | *optional*: `{}`
  | *extension*: `{}`
  | *glob*: `{}`
  | *dir*: `{}`







**gff_invert**::
    {}

  | *type*: `map`
  | *source*: `input`
  | *category*: `output`
  | *optional*: `{}`
  | *extension*: `{}`
  | *glob*: `{}`
  | *dir*: `{}`







**input**::
    Sequences to map

  | *type*: `map`
  | *source*: `{}`
  | *category*: `input`
  | *optional*: `False`
  | *extension*: `{}`
  | *glob*: `{}`
  | *dir*: `{}`







**raw**::
    {}

  | *type*: `map`
  | *source*: `input`
  | *category*: `output`
  | *optional*: `{}`
  | *extension*: `{}`
  | *glob*: `{}`
  | *dir*: `{}`






Parameters
~~~~~~~~~~



**db**::
    Gmap db

  | *type*: `file`
  | *default*: ``
  | *optional*: `False`



**default_command**::
    command to run for this template

  | *type*: `{}`
  | *default*: `run`
  | *optional*: `True`



**extra_parameters**::
    extra parameters to feed to gmap

  | *type*: `string`
  | *default*: ``
  | *optional*: `True`



**gff_source**::
    Source field to use in the output GFF

  | *type*: `string`
  | *default*: `gmap`
  | *optional*: `True`



**invert_gff**::
    Invert the GFF (T/*F*)

  | *type*: `set`
  | *default*: `T`
  | *optional*: `True`



**title**::
    A name for this job

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



