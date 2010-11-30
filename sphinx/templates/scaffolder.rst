scaf
------------------------------------------------

**Scaffolder** - Scaffold a set of input files based on a blast against a reference sequence. This software is written around bambus

Commands
~~~~~~~~

**clean**
  Remove all job data, not the Moa job itself, note that this must be implemented by the template.


**run**
  *no help defined*





Parameters
~~~~~~~~~~



**input_file** - input file with the sequences to scaffold
  | *type*: `file`
  | *default*: ``
  | *optional*: `False`



**prefix** - prefix for scaffolding output files
  | *type*: `string`
  | *default*: `scaffolds`
  | *optional*: `True`



**reference_file** - blast database of the reference set
  | *type*: `file`
  | *default*: ``
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



