bamextract
------------------------------------------------

**bamextract**


    Extract a region from a BAM file



Commands
~~~~~~~~

**clean**
  Remove all job data, not the Moa job itself, note that this must be implemented by the template.
  
  
**run**
  Extract a region from a BAM file
  
  

Filesets
~~~~~~~~


**bam**
  BAM input


  | *type*: `single`
  | *category*: `input`
  | *optional*: `False`
  | *pattern*: `{}`




**regions**
  List with regions to extract (id seqid start stop)


  | *type*: `single`
  | *category*: `input`
  | *optional*: `False`
  | *pattern*: `{}`




**vcf**
  optional VCF input


  | *type*: `single`
  | *category*: `input`
  | *optional*: `True`
  | *pattern*: `{}`





Parameters
~~~~~~~~~~



**flank**
  flanking region to extract

  | *type*: `integer`
  | *default*: `100`
  | *optional*: `{}`



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
