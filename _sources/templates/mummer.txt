mummer
------------------------------------------------

**mummer**


    Run mummer between two sequences



Commands
~~~~~~~~

**clean**
  Remove all job data, not the Moa job itself, note that this must be implemented by the template.
  
  
**run**
  *no help defined*
  
  

Filesets
~~~~~~~~


**mum_input_a**
  Set 1 input fasta files





**mum_input_b**
  Set 1 input fasta files






Parameters
~~~~~~~~~~



**mum_breaklen**
  Set the distance an alignment extension will attempt to extend poor scoring regions before giving up (default 200)

  | *type*: `integer`
  | *default*: `200`
  | *optional*: `True`



**mum_matchmode**
  use all matching fragments (max) or only unique matchers (mum)

  | *type*: `set`
  | *default*: `mum`
  | *optional*: `True`



**mum_plot_raw**
  plot an alternative visualization where mummer does not attempt to put the sequences in the correct order

  | *type*: `set`
  | *default*: `F`
  | *optional*: `True`



**mum_self**
  mummer against self

  | *type*: `set`
  | *default*: `T`
  | *optional*: `True`



miscellaneous
~~~~~~~~~~~~~

**Backend**
  gnumake
**Author**
  Mark Fiers
**Creation date**
  Wed Nov 10 07:56:48 2010
**Modification date**
  Wed Nov 10 07:56:48 2010
