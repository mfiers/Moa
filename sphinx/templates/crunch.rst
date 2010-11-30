crunch
------------------------------------------------

**Create ACT crunch files for use with Artemis ACT** - Create a crunch file for use with the Artemis ACT comparison tool.

Commands
~~~~~~~~

**clean**
  Remove all job data, not the Moa job itself, note that this must be implemented by the template.


**run**
  create crunch files





Filesets
~~~~~~~~




**input** - Directory with input fasta files

  | *type*: `input`
  | *category*: `input`
  | *optional*: `False`
  | *extension*: `fasta`
  | *glob*: `{}`






Parameters
~~~~~~~~~~



**eval** - e value cutoff
  | *type*: `float`
  | *default*: `1e-10`
  | *optional*: `True`



**nothreads** - threads to run crunch with (note the overlap with the Make -j parameter)
  | *type*: `integer`
  | *default*: `4`
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



