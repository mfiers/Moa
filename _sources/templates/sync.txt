sync
------------------------------------------------

**Sync directories**


    Create this directory in sync with another directory



Commands
~~~~~~~~

**run**
  Sync!
  
  

Parameters
~~~~~~~~~~



**ignore**
  ignore these names (space separated list)

  | *type*: `{}`
  | *default*: ``
  | *optional*: `True`



**original**
  The local directory to use as a source. If the target (based on what is in the source) does not exists, this directory is copied. If the target exists - only the configuration is copied, and all directory contents are left alone. If this parameter is omitted, the directory with the most recently changed moa configuration.

  | *type*: `string`
  | *default*: `{}`
  | *optional*: `True`



**source**
  The directory to keep in sync with

  | *type*: `string`
  | *default*: `{}`
  | *optional*: `False`



miscellaneous
~~~~~~~~~~~~~

**Backend**
  ruff
**Author**
  Mark Fiers
**Creation date**
  Thu, 30 Jun 2011 21:26:19
**Modification date**
  Thu, 30 Jun 2011 21:25:53
