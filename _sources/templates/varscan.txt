varscan
------------------------------------------------

**Varscan**


    Run VARSCAN to detect snps



Commands
~~~~~~~~

**clean**
  Remove all job data, not the Moa job itself, note that this must be implemented by the template.
  
  
**run**
  *no help defined*
  
  

Parameters
~~~~~~~~~~



**extra_params**
  location of varscan.pl, defaults to /usr/lib/perl5/site_perl/5.8.8/varscan.pl

  | *type*: `string`
  | *default*: ``
  | *optional*: `True`



**input_file**
  Varscan input alignments file

  | *type*: `file`
  | *default*: ``
  | *optional*: `True`



**output_name**
  Base name of the output files

  | *type*: `string`
  | *default*: `out`
  | *optional*: `True`



**perl_file**
  the varscan (perl) executable

  | *type*: `file`
  | *default*: ``
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
