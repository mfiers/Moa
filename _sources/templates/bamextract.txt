bamextract
------------------------------------------------

**Bamextract**


    Extract one sequence from a bam file



Commands
~~~~~~~~

**clean**
  Remove all job data, not the Moa job itself, note that this must be implemented by the template.
  
  
**run**
  *no help defined*
  
  

Parameters
~~~~~~~~~~



**bam_input**
  BAM input file

  | *type*: `file`
  | *default*: ``
  | *optional*: `False`



**fasta_file**
  Fasta file with the reference sequence data

  | *type*: `file`
  | *default*: ``
  | *optional*: `False`



**gff_file**
  GFF annotation file to extract data from

  | *type*: `file`
  | *default*: ``
  | *optional*: `True`



**haplotypes**
  No of haplotypes in the sample

  | *type*: `integer`
  | *default*: `2`
  | *optional*: `True`



**seq_id**
  List of sequence ids to extract

  | *type*: `string`
  | *default*: ``
  | *optional*: `False`



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
