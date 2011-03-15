emboss/revseq
------------------------------------------------



::
    Run emboss revseq


Commands
~~~~~~~~

**revseq**
  Run Revseq





Filesets
~~~~~~~~




**input**::
    Input files for revseq

  | *type*: `input`
  | *category*: `{}`
  | *optional*: `False`
  | *extension*: `fasta`
  | *glob*: `{}`







**output**::
    {}

  | *type*: `map`
  | *source*: `input`
  | *category*: `{}`
  | *optional*: `{}`
  | *extension*: `out`
  | *glob*: `{}`
  | *dir*: `./out`






Parameters
~~~~~~~~~~



**circular**::
    Is the sequence linear?

  | *type*: `set`
  | *default*: `N`
  | *optional*: `True`



**default_command**::
    command to run for this template

  | *type*: `{}`
  | *default*: `run`
  | *optional*: `True`



**find**::
    What to output? 0: Translation between stop codons, 1: Translation between start & stop codon, 2: Nucleotide sequence between stop codons; 3: Nucleotide sequence between start and stop codons. Default: 3

  | *type*: `set`
  | *default*: `3`
  | *optional*: `True`



**title**::
    A name for this job

  | *type*: `string`
  | *default*: ``
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



