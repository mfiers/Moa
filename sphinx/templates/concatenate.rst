concatenate
------------------------------------------------

**Concatenate**

::
    Concatenate a set of fasta files into one.


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



**input_dir**::
    Directory with the input data

  | *type*: `directory`
  | *default*: ``
  | *optional*: `False`



**input_extension**::
    Extension of the input files

  | *type*: `string`
  | *default*: `fasta`
  | *optional*: `True`



**name**::
    name of the file, the outputfile will become ./name.fasta

  | *type*: `string`
  | *default*: ``
  | *optional*: `False`



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



