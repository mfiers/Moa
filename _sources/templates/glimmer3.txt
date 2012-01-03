glimmer3
------------------------------------------------

**Glimmer3**


    Predicts (prokaryotic) using glimmer3.



Commands
~~~~~~~~

**clean**
  Remove all job data, not the Moa job itself, note that this must be implemented by the template.
  
  
**run**
  Glimmer3 is a open reading frame discovery program from the EMBOSS [[emboss]] package. It takes a set of input sequences and predicts all open reading frames. Additionally, this template converts the default output (predicted protein sequences) to GFF3.
  
  

Filesets
~~~~~~~~


**cds**
  CDS output files from glimmer3


  | *type*: `map`
  | *source*: `input`
  | *category*: `output`
  | *optional*: `True`
  | *pattern*: `cds/*.fasta`




**gff**
  GFF output files from glimmer3


  | *type*: `map`
  | *source*: `input`
  | *category*: `output`
  | *optional*: `True`
  | *pattern*: `gff/*.gff`




**input**
  Directory with the input files for Glimmer3





**output**
  Raw output files from glimmer3


  | *type*: `map`
  | *source*: `input`
  | *category*: `output`
  | *optional*: `True`
  | *pattern*: `out/*.g3`




**pep**
  peptide output files from glimmer3


  | *type*: `map`
  | *source*: `input`
  | *category*: `output`
  | *optional*: `True`
  | *pattern*: `pep/*.fasta`





Parameters
~~~~~~~~~~



**gene_len**
  Minimum gene length (glimmer3 -g/--gene_len)

  | *type*: `integer`
  | *default*: `110`
  | *optional*: `True`



**gff_source**
  source field to use in the gff. Defaults to "glimmer3"

  | *type*: `string`
  | *default*: `glimmer3`
  | *optional*: `True`



**max_overlap**
  Maximum overlap, see the glimmer documentation for the -o or --max_olap parameter

  | *type*: `integer`
  | *default*: `50`
  | *optional*: `True`



**stop_codons**
  stop codons

  | *type*: `{}`
  | *default*: `tag,tga,taa,nnn,tnn,ann,gnn,cnn`
  | *optional*: `True`



**treshold**
  treshold for calling a gene a gene (glimmer3 -t)

  | *type*: `integer`
  | *default*: `30`
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
