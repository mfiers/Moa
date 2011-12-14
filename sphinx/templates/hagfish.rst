hagfish
------------------------------------------------

**Run hagfish_extract & hagfish_combine**


    Run the preparatory steps for hagfish



Commands
~~~~~~~~

**circos**
  convert to circos histogram data
  
  
**clean**
  remove all Hagfish files
  
  
**combine**
  *no help defined*
  
  
**report**
  *no help defined*
  
  
**run**
  Run hagfish
  
  

Filesets
~~~~~~~~


**input**
  "hagfish" input files





**output**
  "hagfish" output files


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
