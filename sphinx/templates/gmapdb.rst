gmapdb
------------------------------------------------

**gmapdb index builder** - Builds gmapdb index from a reference sequence

Commands
~~~~~~~~

**clean**
  Remove all job data, not the Moa job itself, note that this must be implemented by the template.


**run**
  *no help defined*





Parameters
~~~~~~~~~~



**input_dir** - The reference sequence to build a gmap database with.
  | *type*: `directory`
  | *default*: ``
  | *optional*: `False`



**input_extension** - Extension of the input files, defaults to fasta
  | *type*: `string`
  | *default*: `fasta`
  | *optional*: `True`



**name** - Name of the gmap index to create
  | *type*: `string`
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



