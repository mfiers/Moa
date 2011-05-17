lftp
------------------------------------------------

**lftp**


    Use LFTP to download files. This template has two modi, one is set lftp_mode to mirror data, in which case both lftp_url and lftp_pattern (default *) are used. The other modus is lftp_mode=get, when one file defined by lftp_url is downloaded. In the mirror mode it is possible to download only those files that are newer as the files already downloaded by using the lftp_timestamp parameter



Commands
~~~~~~~~

**clean**
  Remove all job data, not the Moa job itself, note that this must be implemented by the template.
  
  
**run**
  execute the download
  
  

Parameters
~~~~~~~~~~



**dos2unix**
  Run dos2unix to prevent problems with possible dos text files

  | *type*: `set`
  | *default*: `F`
  | *optional*: `True`



**get_name**
  target name of the file to download

  | *type*: `string`
  | *default*: ``
  | *optional*: `True`



**lftp_output_dir**
  subdir to create & write all output to. If not defined, data will be downloaded to directory containing the Makefile

  | *type*: `directory`
  | *default*: `.`
  | *optional*: `{}`



**lock**
  Lock this job after running. This means that you will have to manually unlock the job before lftp actually reruns. This is a good choice if your downloading large datasets or have a slow connection

  | *type*: `set`
  | *default*: `T`
  | *optional*: `True`



**mode**
  Mode of operation - mirror or get. Mirror enables timestamping. Get just gets a single file. If using get, consider setting depend_lftp_timestamp to F. When using get, the full url should be in lftp_url. lftp_pattern is ignored. Defaults to mirror.

  | *type*: `set`
  | *default*: `get`
  | *optional*: `True`



**noclean**
  set of files not to be deleted by the powerclean

  | *type*: `string`
  | *default*: `moa.mk Makefile`
  | *optional*: `True`



**pass**
  password for the remote site, note that this can be defined on the commandline using: make lftp_pass=PASSWORD

  | *type*: `password`
  | *default*: ``
  | *optional*: `True`



**pattern**
  glob pattern to download

  | *type*: `string`
  | *default*: `'*'`
  | *optional*: `True`



**powerclean**
  Do brute force cleaning (T/F). Remove all files, except moa.mk & Makefile when calling make clean. Defaults to F.

  | *type*: `set`
  | *default*: `F`
  | *optional*: `True`



**timestamp**
  Depend on lftp to decide if a file needs updating, else a touchfile is created that you need to delete or touch before updating (T/*F*)

  | *type*: `set`
  | *default*: `F`
  | *optional*: `True`



**url**
  The base url to download from

  | *type*: `string`
  | *default*: ``
  | *optional*: `True`



**user**
  username for the remote site

  | *type*: `string`
  | *default*: ``
  | *optional*: `True`



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
