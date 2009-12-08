title=filter sequences that will give a hit from TAIR9 - improves the speed of this run
g_input_dir=../../10.download/20.arabidopsis.proteome/
g_input_pattern=TAIR9_pep_*
g_name_sed=s/.*/TAIR9_filtered/
g_process=fastaExtract -f $< -l hitlist >> $(g_target)
moa_precommand=rm TAIR9_filtered || true
