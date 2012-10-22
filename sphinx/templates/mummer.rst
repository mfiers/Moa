mummer
------------------------------------------------

**mummer**


    Run mummer between two sequences



Commands
~~~~~~~~

**clean**
  Remove all job data, not the Moa job itself, note that this must be implemented by the template.
  
  
**run**
  Run mummer
  
  

Filesets
~~~~~~~~


**input**
  Set 1 input fasta files





**reference**
  Set 1 input fasta files






Parameters
~~~~~~~~~~



**base**
  base name for all generated files

  | *type*: `{}`
  | *default*: `out`
  | *optional*: `True`



**breaklen**
  Set the distance an alignment extension will attempt to extend poor scoring regions before giving up (default 200)

  | *type*: `integer`
  | *default*: `200`
  | *optional*: `True`



**genomecenter**
  genome center - used in the AGP file

  | *type*: `{}`
  | *default*: `pflnz`
  | *optional*: `True`



**gff_source**
  GFF source field

  | *type*: `{}`
  | *default*: `mumscaff`
  | *optional*: `True`



**linker**
  linker sequence for the merged output sequence

  | *type*: `{}`
  | *default*: `NNNNNNCTAGCTAGCATGNNNNNN`
  | *optional*: `True`



**matchmode**
  use all matching fragments (max) or only unique matchers (mum)

  | *type*: `set`
  | *default*: `mum`
  | *optional*: `True`



**mum_plot_raw**
  plot an alternative visualization where mummer does not attempt to put the sequences in the correct order

  | *type*: `boolean`
  | *default*: `False`
  | *optional*: `True`



**organism**
  Organism name - used in the AGP file

  | *type*: `{}`
  | *default*: ``
  | *optional*: `True`



**taxid**
  Taxonomy id - used in the AGP file

  | *type*: `{}`
  | *default*: ``
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
