soap_aln_se
------------------------------------------------



::
    Use SOAP to align a set of fastq reads against a db


Commands
~~~~~~~~

**clean**
  Remove all job data, not the Moa job itself


**run**
  run soap to align single end reads





Filesets
~~~~~~~~




**fq_input**::
    Fastq input file

  | *type*: `input`
  | *category*: `input`
  | *optional*: `False`
  | *extension*: `fq`
  | *glob*: `*`







**sam_output**::
    {}

  | *type*: `map`
  | *source*: `fq_input`
  | *category*: `output`
  | *optional*: `{}`
  | *extension*: `sam`
  | *glob*: `{}`
  | *dir*: `.`







**soap_output**::
    {}

  | *type*: `map`
  | *source*: `fq_input`
  | *category*: `output`
  | *optional*: `{}`
  | *extension*: `soap`
  | *glob*: `{}`
  | *dir*: `.`






Parameters
~~~~~~~~~~



**db_index_files**::
    Prefix name for reference index [*.index]

  | *type*: `string`
  | *default*: ``
  | *optional*: `False`



**edge_bp_no_gaps**::
    will not allow gap exist inside n-bp edge of a read

  | *type*: `integer`
  | *default*: `5`
  | *optional*: `True`



**gap_size**::
    one continuous gap size allowed on a read

  | *type*: `integer`
  | *default*: `0`
  | *optional*: `True`



**how_report_hits**::
    How  to  report repeat hits, 0=none; 1=random one; 2=all

  | *type*: `integer`
  | *default*: `1`
  | *optional*: `True`



**long_read_seed_len**::
    For  long  reads  with  high  error rate at 3'-end, those can't align whole length, then  first  align  5'  INT  bp subsequence as a seed, [256] use whole length of the read

  | *type*: `integer`
  | *default*: `256`
  | *optional*: `True`



**match_mode**::
    Match mode for each read or the seed part of read,  which shouldn't contain more than 2 mismaches, 0 exact match only 1 1 mismatch match only 2 2 mismatch match only 3 [gap] (coming soon) 4 find the best hits

  | *type*: `integer`
  | *default*: `4`
  | *optional*: `True`



**mismatches_per_read**::
    Totally allowed mismatches in one read

  | *type*: `integer`
  | *default*: `6`
  | *optional*: `True`



**out_read_id**::
    Output reads id instead of reads name

  | *type*: `boolean`
  | *default*: `False`
  | *optional*: `True`



**out_unmapped_reads_file**::
    Output file name for unmapped reads

  | *type*: `string`
  | *default*: `unmapped_reads.txt`
  | *optional*: `True`



**rm_low_qual_reads**::
    Filter low quality reads contain more INT bp Ns

  | *type*: `integer`
  | *default*: `5`
  | *optional*: `True`



**thread_num**::
    Multithreads, n threads

  | *type*: `integer`
  | *default*: `1`
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
  Mark Fiers, Yogini Idnani
**Creation date**
  Wed Nov 29 07:56:48 2010
**Modification date**
  1291085573.25



