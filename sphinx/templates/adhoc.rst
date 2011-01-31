adhoc
------------------------------------------------

**Execute an ad hoc analysis**

::
    The ad hoc template aids in executing a one line on a set of input files.


Commands
~~~~~~~~

**clean**
  Remove all job data, not the Moa job itself, note that this must be implemented by the template.


**run**
  *no help defined*





Filesets
~~~~~~~~




**input**::
    Input files for adhoc

  | *type*: `map`
  | *source*: `{}`
  | *category*: `input`
  | *optional*: `True`
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



**mode**::
     operation mode: *seq*, sequential: process the input files one by one; *par*, parallel: process the input files in parallel (use with `-j`); *all*: process all input files at once (use `$^` in `adhoc_process`) and *simple*: Ignore input files, just execute `adhoc_process` once.

  | *type*: `set`
  | *default*: `seq`
  | *optional*: `True`



**name_sed**::
    A sed expression which can be used to derive the output file name for each input file (excluding the path). The sed expression is executed for each input file name, and the result is available as $t in the $(adhoc_process) statement. Make sure that you use single quotes when specifying this on the command line

  | *type*: `string`
  | *default*: `s/a/a/`
  | *optional*: `True`



**output_dir**::
    Output subdirectory

  | *type*: `directory`
  | *default*: `.`
  | *optional*: `True`



**process**::
    Command to execute for each input file. The path to the input file is available as $< and the output file as $t. (it is not mandatory to use both parameters, for example "cat $< > output" would concatenate all files into one big file

  | *type*: `string`
  | *default*: `echo "needs a sensbile command"`
  | *optional*: `True`



**title**::
    A name for this job

  | *type*: `string`
  | *default*: ``
  | *optional*: `True`



**touch**::
    use touch files to track if input files have changed.

  | *type*: `set`
  | *default*: `T`
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



