soapdb
------------------------------------------------

**Bowtie index builder**

::
    Builds a bowtie index from a reference sequence


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



**input_fasta**::
    input fasta file for the database

  | *type*: `file`
  | *default*: `{}`
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
  Mark Fiers, Yogini Idnani
**Creation date**
  Wed Nov 10 07:56:48 2010
**Modification date**
  Wed Nov 10 07:56:48 2010



