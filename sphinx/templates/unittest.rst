unittest
------------------------------------------------




    Template used in testing - has no other purpose



Commands
~~~~~~~~

**clean**
  Remove all job data
  
  
**prepare**
  prepare for the unittest
  
  
**run**
  Prepare & Run
  
  
  **run** delegates execution to: **prepare, run2**
  
**run2**
  actually run
  
  

Filesets
~~~~~~~~


**input_1**
  Input file set 1





**input_2**
  Input file set 2


  | *type*: `map`
  | *source*: `input_1`
  | *category*: `input`
  | *optional*: `{}`
  | *pattern*: `in2/*_2.txt`




**output**
  output files


  | *type*: `map`
  | *source*: `input_1`
  | *category*: `output`
  | *optional*: `{}`
  | *pattern*: `./*.out`





Parameters
~~~~~~~~~~



**test_string**
  Test string values

  | *type*: `string`
  | *default*: `{}`
  | *optional*: `True`



miscellaneous
~~~~~~~~~~~~~

**Backend**
  ruff
**Author**
  Yogini Idnani, Mark Fiers
**Creation date**
  Wed Nov 25 17:06:48 2010
**Modification date**
  unknown
