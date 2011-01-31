blast
------------------------------------------------

**Basic Local Alignment Tool**

::
    Wraps BLAST [[Alt90]], probably the most popular similarity search tool in bioinformatics.


Commands
~~~~~~~~

**blast_report**
  Generate a text BLAST report.


**clean**
  Remove all job data, not the Moa job itself, note that this must be implemented by the template.


**prepare**
  *no help defined*


**run**
  Running BLAST takes an input directory, determines what sequences are present and executes BLAST on each of these. Moa BLAST is configured to create XML output (as opposed to the standard text based output) in the out directory. The output XML is subsequently converted to GFF3 by the custom blast2gff script (using BioPython). Additionally, a simple text report is created.


**run2**
  *no help defined*





Filesets
~~~~~~~~




**db**::
    Blast database

  | *type*: `map`
  | *source*: `{}`
  | *category*: `prerequisite`
  | *optional*: `False`
  | *extension*: `{}`
  | *glob*: `{}`
  | *dir*: `{}`







**input**::
    Directory with the input files for BLAST, in Fasta format

  | *type*: `map`
  | *source*: `{}`
  | *category*: `input`
  | *optional*: `False`
  | *extension*: `{}`
  | *glob*: `{}`
  | *dir*: `{}`







**outgff**::
    {}

  | *type*: `map`
  | *source*: `input`
  | *category*: `output`
  | *optional*: `True`
  | *extension*: `{}`
  | *glob*: `{}`
  | *dir*: `{}`







**output**::
    {}

  | *type*: `map`
  | *source*: `input`
  | *category*: `output`
  | *optional*: `True`
  | *extension*: `{}`
  | *glob*: `{}`
  | *dir*: `{}`






Parameters
~~~~~~~~~~



**default_command**::
    command to run for this template

  | *type*: `{}`
  | *default*: `run`
  | *optional*: `True`



**eval**::
    e value cutoff

  | *type*: `float`
  | *default*: `1e-10`
  | *optional*: `True`



**gff_blasthit**::
    (T,**F**) - export an extra blasthit feature to the created gff, grouping all hsp (match) features.

  | *type*: `set`
  | *default*: `F`
  | *optional*: `True`



**gff_source**::
    source field to use in the gff

  | *type*: `string`
  | *default*: `BLAST`
  | *optional*: `True`



**nohits**::
    number of hits to report

  | *type*: `integer`
  | *default*: `50`
  | *optional*: `True`



**nothreads**::
    threads to run blast with (note the overlap with the Make -j parameter)

  | *type*: `integer`
  | *default*: `2`
  | *optional*: `True`



**program**::
    blast program to use (default: blastn)

  | *type*: `set`
  | *default*: `blastn`
  | *optional*: `True`



**title**::
    A name for this job

  | *type*: `string`
  | *default*: ``
  | *optional*: `False`



Other
~~~~~

**Backend**
  ruff
**Author**
  Mark Fiers
**Creation date**
  Wed Nov 10 07:56:48 2010
**Modification date**
  Wed Nov 10 07:56:48 2010



