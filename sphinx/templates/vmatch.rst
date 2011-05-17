vmatch
------------------------------------------------

**Vmatch**


    Run VMATCH on an set of input files (query) vs a database index.



Commands
~~~~~~~~

**clean**
  Remove all job data, not the Moa job itself, note that this must be implemented by the template.
  
  
**run**
  *no help defined*
  
  

Parameters
~~~~~~~~~~



**db**
  vmatch db to compare against

  | *type*: `file`
  | *default*: ``
  | *optional*: `True`



**extra_parameters**
  extra parameters to feed to vmatch

  | *type*: `string`
  | *default*: ``
  | *optional*: `True`



**input_file**
  input file with the sequences to map

  | *type*: `file`
  | *default*: ``
  | *optional*: `True`



miscellaneous
~~~~~~~~~~~~~

**Backend**
  gnumake
**Author**
  Mark Fiers
**Creation date**
  Wed Nov 10 07:56:48 2010
**Modification date**
  Wed Nov 10 07:56:48 2010
