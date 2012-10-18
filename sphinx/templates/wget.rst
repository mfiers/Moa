wget
------------------------------------------------

**wget**


    Use WGET to download files. This template has two modi, one is set wget_mode to mirror data, in which case both wget_url and wget_pattern (default *) are used.  The other modus is wget_mode=get, when one file defined by wget_url is downloaded.  In the mirror mode it is possible to download only those files that are newer as the files already downloaded by using the wget_timestamp parameter



Commands
~~~~~~~~

**run**
  Download
  
  

Parameters
~~~~~~~~~~



**pass**
  Password for the remote site (note - this is not very safe, the password will be stored in plan text

  | *type*: `password`
  | *default*: ``
  | *optional*: `True`



**url**
  The url of the file to download

  | *type*: `string`
  | *default*: `{}`
  | *optional*: `False`



**user**
  Username for the remote site

  | *type*: `string`
  | *default*: ``
  | *optional*: `True`



miscellaneous
~~~~~~~~~~~~~

**Backend**
  ruff
**Author**
  Mark Fiers
**Creation date**
  Thu, 02 Jun 2011 10:22:31 +1200
**Modification date**
  Thu, 02 Jun 2011 10:22:53 +1200
