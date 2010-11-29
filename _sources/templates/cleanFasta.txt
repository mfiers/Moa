clean_fasta
------------------------------------------------

**clean Fasta** - Convert files to unix format and convert all characters that are not an A,C,G,T or N to N.

Commands
~~~~~~~~

**clean**
  Remove all job data, not the Moa job itself, note that this must be implemented by the template.


**run**
  Cleanup of a FASTA file (in place!)





Parameters
~~~~~~~~~~



**cf_input_dir** - Directory with the sequences to run cleanfasta on
  | *type*: `directory`
  | *default*: ``
  | *optional*: `False`



**cf_input_extension** - input file extension
  | *type*: `string`
  | *default*: `fasta`
  | *optional*: `True`



**sed_command** - {}
  | *type*: `string`
  | *default*: `/^>/!s/[^ACGTNacgtn]/N/g`
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



