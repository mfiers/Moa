g_input_dir=../20.arabidopsis.proteome/
g_input_pattern=TAIR*
g_output_dir=out
g_process=fastaSplitter -f $< -o out
title=split the TAIR9 proteins into seperate files
