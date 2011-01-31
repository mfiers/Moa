blat
------------------------------------------------

**Blat**

::
    Run BLAT on an set of input files (query) vs a database.


Commands
~~~~~~~~

**clean**
  Remove all job data, not the Moa job itself, note that this must be implemented by the template.


**run**
  *no help defined*





Parameters
~~~~~~~~~~



**db**::
    type of the database (dna, prot or dnax)

  | *type*: `set`
  | *default*: ``
  | *optional*: `False`



**db_id_list**::
    a sorted list of db ids and descriptions, enhances the report generated

  | *type*: `file`
  | *default*: ``
  | *optional*: `True`



**db_type**::
    type of the database (dna, prot or dnax)

  | *type*: `set`
  | *default*: `dna`
  | *optional*: `True`



**default_command**::
    command to run for this template

  | *type*: `{}`
  | *default*: `run`
  | *optional*: `True`



**eval**::
    evalue cutoff to select the reported hits on (defaults to 1e-15)

  | *type*: `float`
  | *default*: `1e-10`
  | *optional*: `True`



**gff_source**::
    Source field for the generated GFF files

  | *type*: `string`
  | *default*: ``
  | *optional*: `False`



**input_dir**::
    source field in the generated gff

  | *type*: `directory`
  | *default*: ``
  | *optional*: `False`



**input_extension**::
    extension of the input files

  | *type*: `string`
  | *default*: `fasta`
  | *optional*: `True`



**input_file**::
    input query file. If this variable is not defined, the combination of blat_input_dir and blat_input_extension is used to find a list of input files

  | *type*: `file`
  | *default*: ``
  | *optional*: `False`



**query_type**::
    type of the query (dna, rna, prot, dnax or rnax)

  | *type*: `set`
  | *default*: `dna`
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



