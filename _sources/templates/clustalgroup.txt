clustalgroup
------------------------------------------------

**clustalw**

::
    Run clustalw on two sets of sequences


Commands
~~~~~~~~

**clean**
  Remove all job data, not the Moa job itself, note that this must be implemented by the template.


**run**
  run clustalw





Parameters
~~~~~~~~~~



**cwg_input_dir**::
    This set of sequences to run clustalw on

  | *type*: `directory`
  | *default*: ``
  | *optional*: `False`



**cwg_input_extension**::
    Input file extension

  | *type*: `string`
  | *default*: `fasta`
  | *optional*: `True`



**default_command**::
    command to run for this template

  | *type*: `{}`
  | *default*: `run`
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



