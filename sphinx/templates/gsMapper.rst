gsmap
------------------------------------------------

**GSMapper**

::
    Run the Roche GS Reference mapper


Commands
~~~~~~~~

**clean**
  Remove all job data, not the Moa job itself, note that this must be implemented by the template.


**run**
  *no help defined*





Parameters
~~~~~~~~~~



**annotation**::
    Gene annotation file in the UCSC GenePred format

  | *type*: `file`
  | *default*: ``
  | *optional*: `True`



**min_overlap_ident**::
    Minimum identity length in the assembly step

  | *type*: `integer`
  | *default*: `90`
  | *optional*: `True`



**min_overlap_len**::
    Minimum overlap length in the assembly step

  | *type*: `integer`
  | *default*: `40`
  | *optional*: `True`



**name**::
    Name identifying this mapping in the output gff

  | *type*: `string`
  | *default*: ``
  | *optional*: `False`



**reference_fasta**::
    A multifasta file with the reference sequence(s)with the library id.

  | *type*: `file`
  | *default*: ``
  | *optional*: `True`



**sfffile**::
    SFF files with reads to map against the reference sequences

  | *type*: `file`
  | *default*: ``
  | *optional*: `True`



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



