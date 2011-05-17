gather
------------------------------------------------

**gather files**


    gather a set of files and create hardlinks to. Hardlinks have as advantage that updates are noticed via the timestamp. Hence, make recognizes them.



Commands
~~~~~~~~

**clean**
  Remove all job data, not the Moa job itself, note that this must be implemented by the template.
  
  
**run**
  gather files
  
  

Parameters
~~~~~~~~~~



**g_input_dir**
  list of directories with the input files

  | *type*: `directory`
  | *default*: ``
  | *optional*: `False`



**g_input_pattern**
  glob pattern to download

  | *type*: `string`
  | *default*: `*`
  | *optional*: `True`



**g_limit**
  limit the number of files gathered (with the most recent files first, defaults to 1mln)

  | *type*: `integer`
  | *default*: `1000000`
  | *optional*: `True`



**g_name_sed**
  SED expression to be executed on each file name - allows you to change file names

  | *type*: `string`
  | *default*: `s/a/a/`
  | *optional*: `True`



**g_output_dir**
  Output subdirectory, defaults to .

  | *type*: `directory`
  | *default*: `.`
  | *optional*: `True`



**g_parallel**
  allow parallel execution (T) or not (**F**). If for example concatenating to one single file, you should not have multiple threads.

  | *type*: `set`
  | *default*: `F`
  | *optional*: `True`



**g_powerclean**
  Do brute force cleaning (T/F). Remove all files, except moa.mk & Makefile when calling make clean. Defaults to F.

  | *type*: `set`
  | *default*: `F`
  | *optional*: `True`



**g_process**
  Command to process the files. If undefined, hardlink the files.

  | *type*: `string`
  | *default*: `ln -f $$< $$(g_target)`
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
