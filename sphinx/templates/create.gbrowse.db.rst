upload2gbrowse
------------------------------------------------

**Library for uploading data to GBrowse**

::
    A library that aids in uploading FASTA and GFF to a Generic Genome Browser database. This template is only to be used embedded in another template. This library expects that the following variables are preset; gup_fasta_dir, gup_gff_dir gup_upload_fasta, gup_upload_gff


Commands
~~~~~~~~

**clean**
  Remove all job data, not the Moa job itself, note that this must be implemented by the template.


**gupgo**
  *no help defined*


**initGbrowse**
  *no help defined*


**run**
  *no help defined*





Parameters
~~~~~~~~~~



**gup_db**::
    gbrowse database. If not defined, this defaults to moa.

  | *type*: `string`
  | *default*: ``
  | *optional*: `False`



**gup_fasta_extension**::
    extension of the FASTA files to upload (.fasta)

  | *type*: `string`
  | *default*: `fasta`
  | *optional*: `True`



**gup_force_upload**::
    upload to gbrowse, ignore gup_lock and upload all, not only files newer that upload_gff or upload_fasta

  | *type*: `set`
  | *default*: `F`
  | *optional*: `True`



**gup_gff_extension**::
    extension of the GFF files to upload (.gff)

  | *type*: `string`
  | *default*: `gff`
  | *optional*: `True`



**gup_upload_fasta**::
    upload fasta to gbrowse (T/F)

  | *type*: `set`
  | *default*: `F`
  | *optional*: `True`



**gup_upload_gff**::
    upload gff to gbrowse (T/F)

  | *type*: `set`
  | *default*: `F`
  | *optional*: `True`



**gup_user**::
    gbrowse db user. If not defined, this defaults to moa.

  | *type*: `string`
  | *default*: ``
  | *optional*: `False`



**marks_extensions**::
    Add some extensions to the Gbrowse database to be initalized, for use by Mark.

  | *type*: `set`
  | *default*: `F`
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



