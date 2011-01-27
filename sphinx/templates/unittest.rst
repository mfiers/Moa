unittest
------------------------------------------------



::
    Template used in testing - has no other purpose


Commands
~~~~~~~~

**clean**
  Remove all job data


**prepare**
  prepare for the unittest


**run**
  Prepare & Run


**run2**
  actually run





Filesets
~~~~~~~~




**input_1**::
    Input file set 1

  | *type*: `map`
  | *source*: `{}`
  | *category*: `input`
  | *optional*: `True`
  | *extension*: `{}`
  | *glob*: `{}`
  | *dir*: `{}`







**input_2**::
    Input file set 2

  | *type*: `map`
  | *source*: `input_1`
  | *category*: `input`
  | *optional*: `{}`
  | *extension*: `{}`
  | *glob*: `{}`
  | *dir*: `{}`







**output**::
    output files

  | *type*: `map`
  | *source*: `input_1`
  | *category*: `output`
  | *optional*: `{}`
  | *extension*: `{}`
  | *glob*: `{}`
  | *dir*: `{}`






Parameters
~~~~~~~~~~



**default_command**::
    command to run for this template

  | *type*: `{}`
  | *default*: `run`
  | *optional*: `True`



**test_string**::
    Test string values

  | *type*: `string`
  | *default*: `{}`
  | *optional*: `True`



**title**::
    A name for this job

  | *type*: `string`
  | *default*: `unittesting`
  | *optional*: `True`



Other
~~~~~

**Backend**
  ruff
**Author**
  Yogini Idnani, Mark Fiers
**Creation date**
  Wed Nov 25 17:06:48 2010
**Modification date**
  1291933991.17



