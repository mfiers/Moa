cdsmatrix
------------------------------------------------

**CdsMatrix**


    Predicts (prokaryotic) using glimmer3.



Commands
~~~~~~~~

**clean**
  Remove all job data, not the Moa job itself, note that this must be implemented by the template.
  
  
**run**
  Generate a matrix of CDS's
  
  

Filesets
~~~~~~~~


**input**
  Directory with the cds files for Glimmer3





**output**
  Output blast files


  | *type*: `map`
  | *source*: `input`
  | *category*: `output`
  | *optional*: `True`
  | *pattern*: `./*.out`




**reference**
  reference multi fasta file


  | *type*: `single`
  | *category*: `prerequisite`
  | *optional*: `{}`
  | *pattern*: `*/*.fasta`




**table**
  table files


  | *type*: `map`
  | *source*: `input`
  | *category*: `output`
  | *optional*: `True`
  | *pattern*: `./*.tab`





Parameters
~~~~~~~~~~



**cutoff**
  score cutoff value - disregards hits below this score

  | *type*: `{}`
  | *default*: `100`
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
  Thu, 21 Jul 2011 20:31:10 +1200
