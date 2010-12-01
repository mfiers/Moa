bowtiedb
------------------------------------------------

**Bowtie index builder**

::
    Builds a bowtie index from a reference sequence


Commands
~~~~~~~~

**clean**
  Remove all job data, not the Moa job itself, note that this must be implemented by the template.


**run**
  *no help defined*





Filesets
~~~~~~~~




**input**::
    Sequence files used to build a bowtie database

  | *type*: `input`
  | *category*: `input`
  | *optional*: `False`
  | *extension*: `fasta`
  | *glob*: `{}`






Parameters
~~~~~~~~~~



**name**::
    Name of the bowtie index to create

  | *type*: `string`
  | *default*: ``
  | *optional*: `False`



**title**::
    A name for this job

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



