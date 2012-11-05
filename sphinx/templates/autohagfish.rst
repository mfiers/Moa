autohagfish
------------------------------------------------

**Automatically run bowtie & hagfish combined**


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




**fw_fq**
  forward fq input





**outbase**
  basename for output files


  | *type*: `map`
  | *source*: `fw_fq`
  | *category*: `output`
  | *optional*: `True`
  | *pattern*: `./*`




**rev_fq**
  reverse fq input


  | *type*: `map`
  | *source*: `fw_fq`
  | *category*: `input`
  | *optional*: `True`
  | *pattern*: `*/*2.fq`





Parameters
~~~~~~~~~~



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



**threads**
  no threads to use

  | *type*: `integer`
  | *default*: `8`
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
