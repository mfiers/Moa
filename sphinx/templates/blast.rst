blast
------------------------------------------------

**Basic Local Alignment Tool**


    Wraps BLAST [[Alt90]], probably the most popular similarity search tool in bioinformatics.



Commands
~~~~~~~~

**clean**
  Remove all job data, not the Moa job itself, note that this must be implemented by the template.
  
  
**report**
  Generate a text BLAST report.
  
  
**run**
  Running BLAST takes an input directory, determines what sequences are present and executes BLAST on each of these.  Moa BLAST is configured to create XML output (as opposed to the standard text based output) in the out directory. The output XML is subsequently converted to GFF3 by the custom blast2gff script (using BioPython). Additionally, a simple text report is created.
  
  

Filesets
~~~~~~~~


**db**
  Blast database


  | *type*: `single`
  | *category*: `prerequisite`
  | *optional*: `False`
  | *pattern*: `*/*`




**input**
  Directory with the input files for BLAST, in Fasta format





**outgff**
  GFF output files


  | *type*: `map`
  | *source*: `input`
  | *category*: `output`
  | *optional*: `True`
  | *pattern*: `gff/*.gff`




**output**
  XML blast output files


  | *type*: `map`
  | *source*: `input`
  | *category*: `output`
  | *optional*: `True`
  | *pattern*: `out/*.out`





Parameters
~~~~~~~~~~



**eval**
  e value cutoff

  | *type*: `float`
  | *default*: `1e-10`
  | *optional*: `True`



**gff_blasthit**
  (T,**F**) - export an extra blasthit feature to the created gff, grouping all hsp (match) features.

  | *type*: `set`
  | *default*: `F`
  | *optional*: `True`



**gff_source**
  source field to use in the gff

  | *type*: `string`
  | *default*: `BLAST`
  | *optional*: `True`



**nohits**
  number of hits to report

  | *type*: `integer`
  | *default*: `50`
  | *optional*: `True`



**nothreads**
  threads to run blast with (note the overlap with the Make -j parameter)

  | *type*: `integer`
  | *default*: `2`
  | *optional*: `True`



**program**
  blast program to use (default: blastn)

  | *type*: `set`
  | *default*: `blastn`
  | *optional*: `True`



miscellaneous
~~~~~~~~~~~~~

**Backend**
  ruff
**Author**
  Mark Fiers
**Creation date**
  Wed Nov 10 07:56:48 2010
**Modification date**
  Wed Nov 10 07:56:48 2010
