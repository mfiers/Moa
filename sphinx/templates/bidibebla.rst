bdbb
------------------------------------------------

**Bidirectional best BLAST hit** - Discover the bidirectional best blast hit between two sets of sequences

Commands
~~~~~~~~

**clean**
  Remove all job data, not the Moa job itself, note that this must be implemented by the template.


**run**
  generate a list of bidirectional best blast hits.





Parameters
~~~~~~~~~~



**eval** - e value cutoff
  | *type*: `float`
  | *default*: `1e-10`
  | *optional*: `True`



**input_file_a** - First multifasta input file
  | *type*: `file`
  | *default*: ``
  | *optional*: `False`



**input_file_b** - First multifasta input file
  | *type*: `file`
  | *default*: ``
  | *optional*: `False`



**nothreads** - threads to run bdbb with (note the overlap with the Make -j parameter)
  | *type*: `integer`
  | *default*: `4`
  | *optional*: `True`



**protein** - Are we looking at proteins?
  | *type*: `set`
  | *default*: `F`
  | *optional*: `True`



**title** - A name for this job
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



