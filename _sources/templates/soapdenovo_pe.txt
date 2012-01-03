soapdenovo_pe
------------------------------------------------




    Run Soapdenovo



Commands
~~~~~~~~

**clean**
  Remove all job data
  
  
**run**
  Execute soapdenovo in paired-end mode
  
  

Filesets
~~~~~~~~


**fq_forward**
  fastq input files directory - forward





**fq_reverse**
  fastq input files directory - reverse


  | *type*: `map`
  | *source*: `fq_forward`
  | *category*: `input`
  | *optional*: `True`
  | *pattern*: `*/*_2.fq`




**output**
  soap denovo output file


  | *type*: `single`
  | *category*: `output`
  | *optional*: `True`
  | *pattern*: `{}`





Parameters
~~~~~~~~~~



**avg_insert**
  library insert size

  | *type*: `integer`
  | *default*: `200`
  | *optional*: `{}`



**executable**
  which executable to use (SOAPdenovo-127mer, SOAPdenovo-31mer or SOAPdenovo-63mer)

  | *type*: `{}`
  | *default*: `SOAPdenovo-31mer`
  | *optional*: `True`



**kmer**
  kmer size

  | *type*: `integer`
  | *default*: `31`
  | *optional*: `True`



**skip_config_file**
  skip automatic config file generation - if you skip this, make sure that you have a soap.config configuration file in the current directory

  | *type*: `boolean`
  | *default*: `False`
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
  Mon, 21 Nov 2011 12:47:16
**Modification date**
  Mon, 21 Nov 2011 12:47:22
