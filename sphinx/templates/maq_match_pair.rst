maqpair
------------------------------------------------

**MAQ paired ends mapper**

::
    Map paired ends to a reference sequence using MAQ


Commands
~~~~~~~~

**clean**
  Remove all job data, not the Moa job itself, note that this must be implemented by the template.


**run**
  *no help defined*





Parameters
~~~~~~~~~~



**default_command**::
    command to run for this template

  | *type*: `{}`
  | *default*: `run`
  | *optional*: `True`



**forward_suffix**::
    Suffix of each forward filename - recognize forward files this way. Note this is not a regular extension, no . is assumed between the filename & suffix

  | *type*: `string`
  | *default*: `_f.bfq`
  | *optional*: `True`



**maxdist**::
    max outer distance for a (non RF) readpair. This applies to illumina matepairs - i.e. short inserts

  | *type*: `integer`
  | *default*: `250`
  | *optional*: `True`



**read_dir**::
    directory containing the forward reads

  | *type*: `string`
  | *default*: ``
  | *optional*: `False`



**reference**::
    Reference bfa file to map the reads to

  | *type*: `string`
  | *default*: ``
  | *optional*: `False`



**reverse_suffix**::
    suffix of reverse files

  | *type*: `string`
  | *default*: `_r.bfq`
  | *optional*: `True`



**RF_maxdist**::
    max outer distance for an RF readpair (corresponds to the -A parameter). This applies to long insert illumina pairs

  | *type*: `integer`
  | *default*: `15000`
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



