soap_aln_pe
------------------------------------------------



::
    Use SOAP to align a set of paired fastq reads against a db


Commands
~~~~~~~~

**clean**
  Remove all job data, not the Moa job itself


**run**
  run soap to align paired end reads





Filesets
~~~~~~~~




**bam_output**::
    {}

  | *type*: `map`
  | *source*: `fq_forward_input`
  | *category*: `output`
  | *optional*: `{}`
  | *extension*: `{}`
  | *glob*: `{}`
  | *dir*: `{}`







**fa_input**::
    directory with reference fasta file name

  | *type*: `map`
  | *source*: `{}`
  | *category*: `prerequisite`
  | *optional*: `False`
  | *extension*: `{}`
  | *glob*: `{}`
  | *dir*: `{}`







**fq_forward_input**::
    fastq input files directory - forward files

  | *type*: `map`
  | *source*: `{}`
  | *category*: `input`
  | *optional*: `False`
  | *extension*: `{}`
  | *glob*: `{}`
  | *dir*: `{}`







**fq_reverse_input**::
    fastq input files directory - reverse files

  | *type*: `map`
  | *source*: `fq_forward_input`
  | *category*: `input`
  | *optional*: `{}`
  | *extension*: `{}`
  | *glob*: `{}`
  | *dir*: `{}`







**soap_output**::
    {}

  | *type*: `map`
  | *source*: `fq_forward_input`
  | *category*: `output`
  | *optional*: `{}`
  | *extension*: `{}`
  | *glob*: `{}`
  | *dir*: `{}`






Parameters
~~~~~~~~~~



**db_index_files**::
    Prefix name for reference index [*.index]

  | *type*: `string`
  | *default*: ``
  | *optional*: `False`



**default_command**::
    command to run for this template

  | *type*: `{}`
  | *default*: `run`
  | *optional*: `True`



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



**max_insert_size**::
    maximal insert size allowed

  | *type*: `integer`
  | *default*: `600`
  | *optional*: `True`



**min_insert_size**::
    minimal insert size allowed

  | *type*: `integer`
  | *default*: `400`
  | *optional*: `True`



**mismatches_per_read**::
    Totally allowed mismatches in one read

  | *type*: `integer`
  | *default*: `6`
  | *optional*: `True`



**out_file_unpaired_aln**::
    output file of unpaired alignment hits

  | *type*: `string`
  | *default*: `unpaired_aln.txt`
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



**report_read_mismatches**::
    report all mismatched reads in SOAP Format

  | *type*: `boolean`
  | *default*: `False`
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



**type_of_pe**::
    for long insert size of pair end reads RF (default means FR pair)

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
  Wed Nov 30 07:56:48 2010
**Modification date**
  1297380110.93



