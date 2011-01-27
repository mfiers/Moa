adhoc2
------------------------------------------------

**Execute an ad hoc analysis**

::
    The adhoc2 template aids in executing a one line on a set of input files.


Commands
~~~~~~~~

**runmap**
  *no help defined*


**runsimple**
  *no help defined*





Filesets
~~~~~~~~




**input**::
    Input files for adhoc

  | *type*: `map`
  | *source*: `{}`
  | *category*: `input`
  | *optional*: `True`
  | *extension*: `{}`
  | *glob*: `{}`
  | *dir*: `{}`







**output**::
    adhoc output files

  | *type*: `map`
  | *source*: `{}`
  | *category*: `output`
  | *optional*: `True`
  | *extension*: `{}`
  | *glob*: `{}`
  | *dir*: `{}`






Parameters
~~~~~~~~~~



**command**::
    Command to execute for each input file. The path to the input file is available as $in and the output file as $out. (it is not mandatory to use both parameters, for example "cat $< > output" would concatenate all files into one big file

  | *type*: `string`
  | *default*: ``
  | *optional*: `False`



**default_command**::
    command to run for this template

  | *type*: `{}`
  | *default*: `run`
  | *optional*: `True`



**title**::
    A name for this job

  | *type*: `string`
  | *default*: ``
  | *optional*: `True`



Other
~~~~~

**Backend**
  ruff
**Author**
  Mark Fiers
**Creation date**
  Wed Nov 10 07:56:48 2010
**Modification date**
  Wed Nov 10 07:56:48 2010



