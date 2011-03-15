kangar_pe
------------------------------------------------



::
    use kangar to pre process raw fq reads


Commands
~~~~~~~~

**clean**
  Remove all job data, not the Moa job itself, note that this must be implemented by the template.


**run**
  run kangar





Filesets
~~~~~~~~




**fq_forward_input**::
    fastq input files - forward - containing the 5' end

  | *type*: `map`
  | *source*: `{}`
  | *category*: `input`
  | *optional*: `False`
  | *extension*: `{}`
  | *glob*: `{}`
  | *dir*: `{}`







**fq_reverse_input**::
    fastq input files directory - reverse - containing the 3' end

  | *type*: `map`
  | *source*: `fq_forward_input`
  | *category*: `input`
  | *optional*: `True`
  | *extension*: `{}`
  | *glob*: `{}`
  | *dir*: `{}`







**output_log**::
    output log file

  | *type*: `map`
  | *source*: `fq_forward_input`
  | *category*: `output`
  | *optional*: `{}`
  | *extension*: `{}`
  | *glob*: `{}`
  | *dir*: `{}`







**rds_output**::
    output rds file

  | *type*: `map`
  | *source*: `fq_forward_input`
  | *category*: `output`
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



**extra_params**::
    any extra parameters

  | *type*: `string`
  | *default*: ``
  | *optional*: `True`



**help**::
    print this help and exit

  | *type*: `boolean`
  | *default*: `False`
  | *optional*: `True`



**mode**::
    processing mode  0 - single end create, 1 - paired end create, 2 - output statistics 3 - dump as fasta

  | *type*: `integer`
  | *default*: `0`
  | *optional*: `True`



**quality**::
    fastq quality scoring- 0 - sanger, 1m - Illumina 1.3+, 2 - Solexa < 1.3, 3 - Ignore quality

  | *type*: `integer`
  | *default*: `3`
  | *optional*: `True`



**reads_num**::
    limit number of reads (or dumps) in each input file to this many, 0 if no limit

  | *type*: `integer`
  | *default*: `0`
  | *optional*: `True`



**rm_duplicates**::
    remove duplicate reads retaining only one

  | *type*: `boolean`
  | *default*: `False`
  | *optional*: `True`



**title**::
    A name for this job

  | *type*: `string`
  | *default*: ``
  | *optional*: `False`



**trim3**::
    trim this number of bases from 3' end of sequence

  | *type*: `integer`
  | *default*: `0`
  | *optional*: `True`



**trim5**::
    trim this number of bases from 5' end of sequence

  | *type*: `integer`
  | *default*: `0`
  | *optional*: `True`



**version**::
    print version information and exit

  | *type*: `boolean`
  | *default*: `False`
  | *optional*: `True`



Other
~~~~~

**Backend**
  ruff
**Author**
  Mark Fiers, Yogini Idnani
**Creation date**
  Wed Nov 10 07:56:48 2010
**Modification date**
  1298158302.29



