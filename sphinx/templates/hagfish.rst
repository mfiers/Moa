hagfish
------------------------------------------------

**Run hagfish_extract & hagfish_combine**


    Run the preparatory steps for hagfish



Commands
~~~~~~~~

**clean**
  remove all Hagfish files
  
  
**finish**
  finish up - find gaps - combine plots - create a report
  
  
**run**
  Run hagfish
  
  

Filesets
~~~~~~~~


**fasta**
  fasta sequence of the reference


  | *type*: `single`
  | *category*: `prerequisite`
  | *optional*: `False`
  | *pattern*: `{}`




**input**
  "hagfish" input files





**output**
  "hagfish" touch files - track what files are done - please do not touch this!


  | *type*: `map`
  | *source*: `input`
  | *category*: `output`
  | *optional*: `True`
  | *pattern*: `./touch/*.touch`





Parameters
~~~~~~~~~~



**circosbinsize**
  Binsize for generating circos formatted histograms

  | *type*: `int`
  | *default*: `{}`
  | *optional*: `True`



**max_ok**
  Maximal acceptable insert size for an aligned pair. If omitted, hagfish will make an estimate

  | *type*: `int`
  | *default*: `0`
  | *optional*: `True`



**min_ok**
  Minimal acceptable insert size for an aligned pair. If omitted, hagfish will make an estimate

  | *type*: `int`
  | *default*: `0`
  | *optional*: `True`



miscellaneous
~~~~~~~~~~~~~

**Backend**
  ruff
**Author**
  Mark Fiers
**Creation date**
  Tue Mar 29 16:34:19 2011
**Modification date**
  Thu, 19 May 2011 20:49:04 +1200
