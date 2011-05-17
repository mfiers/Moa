primersearch
------------------------------------------------

**Run EMBOSS primerpair**


    Search DNA sequences for matches with primer pairs



Commands
~~~~~~~~

**run**
  *no help defined*
  
  

Filesets
~~~~~~~~


**input**
  primersearch input sequence files





**output**
  primersearch output files


  | *type*: `map`
  | *source*: `input`
  | *category*: `output`
  | *optional*: `True`
  | *pattern*: `./*.primersearch`




**primers**
  Primer pairs file


  | *type*: `single`
  | *category*: `prerequisite`
  | *optional*: `False`
  | *pattern*: `*/*`





Parameters
~~~~~~~~~~



**johns_postprocess**
  Run John's Post processing

  | *type*: `boolean`
  | *default*: `True`
  | *optional*: `True`



**mismatch**
  Allowed percent mismatch

  | *type*: `integer`
  | *default*: `0`
  | *optional*: `True`



miscellaneous
~~~~~~~~~~~~~

**Backend**
  ruff
**Author**
  John McCallum
**Creation date**
  Mon Apr 04 08:51:23 2011
**Modification date**
  Mon Apr 04 09:00:42 2011
