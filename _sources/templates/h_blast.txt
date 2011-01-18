h_blast
------------------------------------------------

**Hadoop Blast**

::
    Runs BLAST on a hadoop cluster


Commands
~~~~~~~~

**clean**
  Remove all job data, not the Moa job itself, note that this must be implemented by the template.


**run**
  Similar to a normal blast, but now running on an hadoop cluster





Parameters
~~~~~~~~~~



**db**::
    Location of the blast database

  | *type*: `file`
  | *default*: ``
  | *optional*: `False`



**default_command**::
    command to run for this template

  | *type*: `{}`
  | *default*: `run`
  | *optional*: `True`



**eval**::
    e value cutoff

  | *type*: `float`
  | *default*: `1e-10`
  | *optional*: `True`



**hadoop_base**::
    location of the hadoop installation

  | *type*: `directory`
  | *default*: ``
  | *optional*: `False`



**hdfs_base**::
    htfs://SERVER:PORT for the hdfs filesystem, defaults to "hdfs://localhost:9000"

  | *type*: `string`
  | *default*: `hdfs://localhost:9000`
  | *optional*: `True`



**input_dir**::
    location of the hadoop installation

  | *type*: `directory`
  | *default*: ``
  | *optional*: `False`



**input_extension**::
    input file extension

  | *type*: `string`
  | *default*: `fasta`
  | *optional*: `True`



**nohits**::
    number of hits to report

  | *type*: `integer`
  | *default*: `50`
  | *optional*: `True`



**nothreads**::
    threads to run blast with (note the overlap with the Make -j parameter)

  | *type*: `integer`
  | *default*: `1`
  | *optional*: `True`



**program**::
    blast program to use (default: blastn)

  | *type*: `set`
  | *default*: `blastn`
  | *optional*: `True`



**title**::
    A name for this job

  | *type*: `string`
  | *default*: ``
  | *optional*: `False`



Other
~~~~~

**Backend**
  gnumake
**Author**
  Mark Fiers
**Creation date**
  Wed Nov 10 07:56:48 2010
**Modification date**
  Wed Nov 10 07:56:48 2010



