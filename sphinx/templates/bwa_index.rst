bwa_index
------------------------------------------------

**Bwa index builder** - Builds a bwa index from a reference sequence

Commands
~~~~~~~~

**clean**
  Remove all job data


**run**
  Create the index





Parameters
~~~~~~~~~~



**algorithm** - Algorithm for constructing BWT index. Available options are 'is' and  'bwtsw'
  | *type*: `string`
  | *default*: `is`
  | *optional*: `True`



**color_space** - input sequences are in the color space
  | *type*: `boolean`
  | *default*: `False`
  | *optional*: `True`



**input_fasta** - input fasta file for the database
  | *type*: `file`
  | *default*: `{}`
  | *optional*: `False`



**prefix** - Name of the bwa index to create
  | *type*: `string`
  | *default*: `bwa_index`
  | *optional*: `True`



**title** - A name for this job
  | *type*: `string`
  | *default*: ``
  | *optional*: `False`



Other
~~~~~

**Backend**
  ruff
**Author**
  Mark Fiers, Yogini Idnani
**Creation date**
  Wed Nov 10 07:56:48 2010
**Modification date**
  Wed Nov 10 07:56:48 2010



