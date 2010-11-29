pregap
------------------------------------------------

**Pregap** - Run Pregap. Note that running phrap could be a part of this.

Commands
~~~~~~~~

**clean**
  Remove all job data, not the Moa job itself, note that this must be implemented by the template.


**run**
  *no help defined*





Parameters
~~~~~~~~~~



**cloning_vector** - File containing the cloning vector
  | *type*: `file`
  | *default*: ``
  | *optional*: `False`



**ecoli_screenseq** - File containing ecoli screen sequences
  | *type*: `file`
  | *default*: ``
  | *optional*: `False`



**input_dir** - Directory with the input data
  | *type*: `string`
  | *default*: ``
  | *optional*: `False`



**input_pattern** - file name pattern
  | *type*: `string`
  | *default*: ``
  | *optional*: `False`



**quality_value_clip** - quality cutoff
  | *type*: `integer`
  | *default*: `10`
  | *optional*: `True`



**repeat_masker_lib** - File with a repeatmasker library
  | *type*: `file`
  | *default*: ``
  | *optional*: `False`



**sequencing_vector** - File containing the sequencing vector
  | *type*: `file`
  | *default*: ``
  | *optional*: `False`



**template** - the template pregap config file to use. if not defined, Moa tries ./files/pregap.config.
  | *type*: `file`
  | *default*: `./files/pregap.config.`
  | *optional*: `True`



**title** - A name for this job
  | *type*: `string`
  | *default*: ``
  | *optional*: `False`



**vector_primerfile** - File with the vector primers
  | *type*: `file`
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



