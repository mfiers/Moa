fastx_qual_stats
------------------------------------------------



::
    run fastx_quality_stats, fastq_quality_boxplot_graph.sh and fastx_nucleotide_distribution_graph.sh


Commands
~~~~~~~~

**clean**
  Remove all job data, not the Moa job itself


**run**
  run fastx_quality_stats, fastq_quality_boxplot_graph.sh and fastx_nucleotide_distribution_graph.sh





Filesets
~~~~~~~~




**boxplot_output**::
    {}

  | *type*: `map`
  | *source*: `input`
  | *category*: `output`
  | *optional*: `{}`
  | *extension*: `{}`
  | *glob*: `{}`
  | *dir*: `{}`







**input**::
    fastq input files directory

  | *type*: `map`
  | *source*: `{}`
  | *category*: `input`
  | *optional*: `False`
  | *extension*: `{}`
  | *glob*: `{}`
  | *dir*: `{}`







**nuc_distr_output**::
    {}

  | *type*: `map`
  | *source*: `input`
  | *category*: `output`
  | *optional*: `{}`
  | *extension*: `{}`
  | *glob*: `{}`
  | *dir*: `{}`







**qual_output**::
    {}

  | *type*: `map`
  | *source*: `input`
  | *category*: `output`
  | *optional*: `{}`
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



**gen_postScript_file**::
    Generate PostScript (.PS) file. Default is PNG image.

  | *type*: `boolean`
  | *default*: `False`
  | *optional*: `True`



**graph_title**::
    Title - will be plotted on the graph.

  | *type*: `string`
  | *default*: `{{ input_glob }}`
  | *optional*: `True`



**help**::
    help screen

  | *type*: `boolean`
  | *default*: `False`
  | *optional*: `True`



**new_out_format**::
    New output format (with more information per nucleotide/cycle)

  | *type*: `boolean`
  | *default*: `False`
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
  Wed Dec 03 17:06:48 2010
**Modification date**
  1291933989.56



