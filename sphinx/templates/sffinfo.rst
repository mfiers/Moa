sffinfo
------------------------------------------------

**sffinfo**

::
    Roche sffinfor tool - extract information from sff files


Commands
~~~~~~~~

**clean**
  Remove all job data, not the Moa job itself, note that this must be implemented by the template.


**run**
  Use the Roche sffinfo tool to extract reads, quality scores, flowgrams and accession ids from one or more sff files





Filesets
~~~~~~~~




**accession**::
    {}

  | *type*: `map`
  | *source*: `input`
  | *category*: `output`
  | *optional*: `{}`
  | *extension*: `acc`
  | *glob*: `{}`
  | *dir*: `.`







**flowgram**::
    {}

  | *type*: `map`
  | *source*: `input`
  | *category*: `output`
  | *optional*: `{}`
  | *extension*: `flow`
  | *glob*: `{}`
  | *dir*: `.`







**input**::
    Sff input files

  | *type*: `input`
  | *category*: `input`
  | *optional*: `False`
  | *extension*: `sff`
  | *glob*: `{}`







**quality**::
    {}

  | *type*: `map`
  | *source*: `input`
  | *category*: `output`
  | *optional*: `{}`
  | *extension*: `qual`
  | *glob*: `{}`
  | *dir*: `.`







**sequence**::
    {}

  | *type*: `map`
  | *source*: `input`
  | *category*: `output`
  | *optional*: `{}`
  | *extension*: `reads`
  | *glob*: `{}`
  | *dir*: `.`






Parameters
~~~~~~~~~~



**accessions**::
    Output the accessions

  | *type*: `set`
  | *default*: `T`
  | *optional*: `True`



**flowgrams**::
    output the flowgrams

  | *type*: `set`
  | *default*: `F`
  | *optional*: `True`



**quality**::
    Output quality scores

  | *type*: `set`
  | *default*: `T`
  | *optional*: `True`



**sequences**::
    Output the sequences

  | *type*: `set`
  | *default*: `T`
  | *optional*: `True`



**title**::
    A name for this job

  | *type*: `string`
  | *default*: ``
  | *optional*: `False`



**untrimmed**::
    output untrimmed sequences & qualities

  | *type*: `set`
  | *default*: `F`
  | *optional*: `True`



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



