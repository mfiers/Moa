clustalpair
------------------------------------------------

**clustalw** - Run clustalw on two sets of sequences

Commands
~~~~~~~~

**clean**
  Remove all job data, not the Moa job itself, note that this must be implemented by the template.


**run**
  run clustalw





Parameters
~~~~~~~~~~



**input_dir_a** - This set is compared to the sequences in input_dir_b. only a forward comparison is made (a against b, not the other way round )
  | *type*: `directory`
  | *default*: ``
  | *optional*: `False`



**input_dir_b** - The set to compare against
  | *type*: `directory`
  | *default*: ``
  | *optional*: `False`



**input_extension** - Extension of the input files
  | *type*: `string`
  | *default*: `fasta`
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



