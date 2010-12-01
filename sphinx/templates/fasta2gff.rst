fasta2gff
------------------------------------------------

**GFF from FASTA**

::
    Derive GFF from a FASTA file, usually to accompany the Sequence for upload to a generic genome browser database.


Commands
~~~~~~~~

**clean**
  Remove all job data, not the Moa job itself, note that this must be implemented by the template.


**run**
  *no help defined*





Parameters
~~~~~~~~~~



**f2g_gffsource**::
    Source to be used in the gff

  | *type*: `string`
  | *default*: ``
  | *optional*: `False`



**f2g_input_dir**::
    Directory with the input fasta files

  | *type*: `directory`
  | *default*: ``
  | *optional*: `False`



**f2g_input_extension**::
    glob pattern of the fasta files (default: *.fasta)

  | *type*: `string`
  | *default*: `fasta`
  | *optional*: `True`



**f2g_options**::
    options to be passed to the fasta2gff script

  | *type*: `string`
  | *default*: ``
  | *optional*: `True`



**f2g_output_dir**::
    Directory with the output gff

  | *type*: `directory`
  | *default*: `./gff`
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



