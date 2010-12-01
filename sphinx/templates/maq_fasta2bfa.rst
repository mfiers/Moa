f2b
------------------------------------------------

**Convert fasta to bfa**

::
    Converts a FASTA file to MAQ format for use with a BFA a maq_fasta2bfa index from a reference sequence


Commands
~~~~~~~~

**clean**
  Remove all job data, not the Moa job itself, note that this must be implemented by the template.


**run**
  *no help defined*





Filesets
~~~~~~~~




**bfa**::
    {}

  | *type*: `map`
  | *source*: `input`
  | *category*: `output`
  | *optional*: `{}`
  | *extension*: `bfa`
  | *glob*: `{}`
  | *dir*: `./bfa`







**input**::
    input FASTA files

  | *type*: `input`
  | *category*: `input`
  | *optional*: `False`
  | *extension*: `fasta`
  | *glob*: `{}`






Parameters
~~~~~~~~~~



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



