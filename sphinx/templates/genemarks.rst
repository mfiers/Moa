genemarks
------------------------------------------------

**geneMarkS**

::
    predict genes using geneMarkS


Commands
~~~~~~~~

**clean**
  Remove all job data, not the Moa job itself, note that this must be implemented by the template.


**run**
  *no help defined*





Parameters
~~~~~~~~~~



**default_command**::
    command to run for this template

  | *type*: `{}`
  | *default*: `run`
  | *optional*: `True`



**gff_source**::
    source field to use in the gff. Defaults to "geneMarkS"

  | *type*: `string`
  | *default*: `genemarks`
  | *optional*: `True`



**input_dir**::
    directory containing the input sequences

  | *type*: `directory`
  | *default*: ``
  | *optional*: `False`



**input_extension**::
    input file extension. Defaults to fasta

  | *type*: `string`
  | *default*: `fasta`
  | *optional*: `True`



**matrix**::
    the matrix to use

  | *type*: `file`
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



