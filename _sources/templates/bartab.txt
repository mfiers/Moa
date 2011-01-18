bartab
------------------------------------------------

**Bartab**

::
    BARTAB - a tool to process sff files


Commands
~~~~~~~~

**clean**
  Remove all job data, not the Moa job itself, note that this must be implemented by the template.


**run**
  .. to be written ..





Parameters
~~~~~~~~~~



**default_command**::
    command to run for this template

  | *type*: `{}`
  | *default*: `run`
  | *optional*: `True`



**extra_parameters**::
    extra parameters to feed bartab

  | *type*: `string`
  | *default*: ``
  | *optional*: `True`



**forward_primer**::
    remove forward primer

  | *type*: `string`
  | *default*: ``
  | *optional*: `True`



**in**::
    input file for bartab

  | *type*: `file`
  | *default*: ``
  | *optional*: `False`



**map**::
    A file mapping barcodes to metadata

  | *type*: `file`
  | *default*: ``
  | *optional*: `True`



**min_length**::
    minimun acceptable sequence length

  | *type*: `integer`
  | *default*: `50`
  | *optional*: `True`



**out**::
    base output name

  | *type*: `integer`
  | *default*: `bartab`
  | *optional*: `True`



**qin**::
    Quality scores for the input fasta file

  | *type*: `file`
  | *default*: ``
  | *optional*: `True`



**reverse_primer**::
    remove reverse primer

  | *type*: `string`
  | *default*: ``
  | *optional*: `True`



**title**::
    A name for this job

  | *type*: `string`
  | *default*: ``
  | *optional*: `False`



**trim**::
    Trim barcode

  | *type*: `set`
  | *default*: `T`
  | *optional*: `True`



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



