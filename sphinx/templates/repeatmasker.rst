repmask
------------------------------------------------

**Repeatmasker**

::
    Run a default repeatmask on the input sequences


Commands
~~~~~~~~

**clean**
  Remove all job data, not the Moa job itself, note that this must be implemented by the template.


**run**
  *no help defined*





Filesets
~~~~~~~~




**input**::
    Input files for repmask

  | *type*: `input`
  | *category*: `input`
  | *optional*: `False`
  | *extension*: `fasta`
  | *glob*: `{}`







**output**::
    {}

  | *type*: `map`
  | *source*: `input`
  | *category*: `output`
  | *optional*: `{}`
  | *extension*: `masked`
  | *glob*: `{}`
  | *dir*: `.`







**OUTPUT_FILESET_ID**::
    {}

  | *type*: `map`
  | *source*: `INPUT_FILESET_ID`
  | *category*: `output`
  | *optional*: `{}`
  | *extension*: `OUTPUT_FILETYPE`
  | *glob*: `{}`
  | *dir*: `./OUTPUT_FILETYPE`






Parameters
~~~~~~~~~~



**parallel**::
    No of threads to run in parallel

  | *type*: `integer`
  | *default*: `4`
  | *optional*: `True`



**quick**::
    Quick job

  | *type*: `set`
  | *default*: `F`
  | *optional*: `True`



**simple**::
    Mask *only* low complex/simple repeats, not interspersed repeats (Repeatmasker -(no)int parameter)

  | *type*: `set`
  | *default*: `F`
  | *optional*: `True`



**species**::
    Repeatmasker species

  | *type*: `string`
  | *default*: ``
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



