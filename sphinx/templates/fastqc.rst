fastqc
------------------------------------------------

**Run FastQC for fastq QC**


    Run FastQC on a set a fastq files - quality assessment



Commands
~~~~~~~~

**report**
  Generate a simple fastqc report
  
  
**run**
  *no help defined*
  
  
  **run** delegates execution to: **run2, report**
  
**run2**
  Run Fastqc
  
  

Filesets
~~~~~~~~


**input**
  fastqc input files'





**touch**
  touch files - track if a file has been processed - do not touch this unless you know what you're doing.


  | *type*: `map`
  | *source*: `input`
  | *category*: `output`
  | *optional*: `True`
  | *pattern*: `./*.touch`





Parameters
~~~~~~~~~~



**output_dir**
  output directory for the fastQC report

  | *type*: `dir`
  | *default*: `.`
  | *optional*: `True`



miscellaneous
~~~~~~~~~~~~~

**Backend**
  ruff
**Author**
  Mark Fiers
**Creation date**
  Thu, 28 Apr 2011 09:27:17 +1200
**Modification date**
  Thu, 28 Apr 2011 14:19:04 +1200
