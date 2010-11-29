dottup
------------------------------------------------

**EMBOSS Dottup** - Use dottup (from EMBOSS) to compare two sets of sequences

Commands
~~~~~~~~

**clean**
  Remove all job data, not the Moa job itself, note that this must be implemented by the template.


**run**
  Run dottup





Parameters
~~~~~~~~~~



**input_dir_a** - This set is compared to the sequences in input_dir_b.
  | *type*: `directory`
  | *default*: ``
  | *optional*: `False`



**input_dir_b** - The set to compare against
  | *type*: `directory`
  | *default*: ``
  | *optional*: `True`



**input_extension** - Extension of the dottup input files
  | *type*: `string`
  | *default*: `fasta`
  | *optional*: `True`



**title** - A name for this job
  | *type*: `string`
  | *default*: ``
  | *optional*: `False`



**wordsize** - Wordsize used to discover similarities between sequences
  | *type*: `integer`
  | *default*: `8`
  | *optional*: `True`



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



