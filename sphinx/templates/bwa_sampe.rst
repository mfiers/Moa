bwa_sampe
------------------------------------------------



::
    Generate alignments in SAM format given paired end reads


Commands
~~~~~~~~

**clean**
  Remove all job data, not the Moa job itself


**run**
  run bwa sampe





Filesets
~~~~~~~~




**fq_forward_input**::
    fastq input files directory - forward files

  | *type*: `input`
  | *category*: `input`
  | *optional*: `False`
  | *extension*: `fq`
  | *glob*: `*_1`







**fq_reverse_input**::
    fastq input files directory - reverse files

  | *type*: `map`
  | *source*: `fq_forward_input`
  | *category*: `input`
  | *optional*: `{}`
  | *extension*: `fq`
  | *glob*: `*_2`
  | *dir*: `{{ fq_forward_input_dir }}`







**output**::
    {}

  | *type*: `map`
  | *source*: `fq_forward_input`
  | *category*: `output`
  | *optional*: `{}`
  | *extension*: `sam`
  | *glob*: `{}`
  | *dir*: `.`







**sai_forward_input**::
    sai input files - forward files

  | *type*: `map`
  | *source*: `fq_forward_input`
  | *category*: `input`
  | *optional*: `{}`
  | *extension*: `sai`
  | *glob*: `{{ fq_forward_input_glob }}`
  | *dir*: `.`







**sai_reverse_input**::
    sai input files - reverse files

  | *type*: `map`
  | *source*: `fq_forward_input`
  | *category*: `input`
  | *optional*: `{}`
  | *extension*: `sai`
  | *glob*: `{{ fq_reverse_input_glob }}`
  | *dir*: `{{ sai_forward_input_dir }}`






Parameters
~~~~~~~~~~



**db**::
    bwa database to align against

  | *type*: `string`
  | *default*: ``
  | *optional*: `False`



**disable_insert_size**::
    disable insert size estimate (force -s)

  | *type*: `boolean`
  | *default*: `False`
  | *optional*: `True`



**disable_SW**::
    disable Smith-Waterman for the unmapped mate

  | *type*: `boolean`
  | *default*: `False`
  | *optional*: `True`



**max_aln_out**::
    maximum hits to output for paired reads

  | *type*: `integer`
  | *default*: `3`
  | *optional*: `True`



**max_insert_size**::
    maximum insert size

  | *type*: `integer`
  | *default*: `500`
  | *optional*: `True`



**max_occ_read**::
    maximum occurrences for one end

  | *type*: `integer`
  | *default*: `100000`
  | *optional*: `True`



**max_out_discordant_pairs**::
    maximum hits to output for discordant pairs

  | *type*: `integer`
  | *default*: `10`
  | *optional*: `True`



**preload_index**::
    preload index into memory (for base-space reads only)

  | *type*: `boolean`
  | *default*: `False`
  | *optional*: `True`



**prior_chimeric_rate**::
    prior of chimeric rate (lower bound)

  | *type*: `integer`
  | *default*: `1e-05`
  | *optional*: `True`



**title**::
    A name for this job

  | *type*: `string`
  | *default*: ``
  | *optional*: `False`



Other
~~~~~

**Backend**
  ruff
**Author**
  Yogini Idnani, Mark Fiers
**Creation date**
  Wed Nov 25 17:06:48 2010
**Modification date**
  1291075198.28



