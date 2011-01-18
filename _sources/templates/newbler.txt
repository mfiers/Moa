newbler
------------------------------------------------

**Newbler**

::
    Run a simple, out of the box, newbler assembly. As an extra feature, this template automatically creates uniquely named links to the two main output fasta files (454AllContigs.fna, 454LargeContigs.fna). This is convenient for subsequence gather steps. The links are named after the directory.


Commands
~~~~~~~~

**clean**
  Remove all job data, not the Moa job itself, note that this must be implemented by the template.


**run**
  *no help defined*





Filesets
~~~~~~~~




**input**::
    input SFF files

  | *type*: `map`
  | *source*: `{}`
  | *category*: `input`
  | *optional*: `False`
  | *extension*: `{}`
  | *glob*: `{}`
  | *dir*: `{}`






Parameters
~~~~~~~~~~



**default_command**::
    command to run for this template

  | *type*: `{}`
  | *default*: `run`
  | *optional*: `True`



**largecontig_cutoff**::
    min length of a contig in 454LargeContigs.fna

  | *type*: `integer`
  | *default*: ``
  | *optional*: `True`



**library_name**::
    A library identifier for this assembly. This is used to create an extra fasta file, named using this variable, that contain the generated contigs with their ids prepended with the library id.

  | *type*: `string`
  | *default*: `$(shell echo `basename $(CURDIR)` | sed "s/[ \///\/]//g" )`
  | *optional*: `True`



**mid_configuration**::
    Mid configuration file to use

  | *type*: `file`
  | *default*: ``
  | *optional*: `True`



**mids**::
    mids to use for this assembly

  | *type*: `string`
  | *default*: ``
  | *optional*: `True`



**min_identity**::
    Minimal overalp identity used during assembly

  | *type*: `integer`
  | *default*: ``
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



