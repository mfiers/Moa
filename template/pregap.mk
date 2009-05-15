# lftp a set of files

# Main target - should be first in the file
moa_main_target: check pregap

################################################################################
# Definitions
# targets that the enduser might want to use
moa_targets += pregap clean
pregap_help = Run pregap
clean_help = Clean up. 

# Help
moa_title = Pregap
moa_description = Run Pregap. Note that running phrap could be a part of this. 

# Output definition
moa_outputs += pregap
moa_output_pregap = ./BACS/pregap.output
moa_output_pregap_help = Set of processed BACs

#varables that NEED to be defined
moa_must_define += input_dir
input_dir_help = Directory with the input data

moa_must_define += input_pattern
input_pattern_help = file name pattern

moa_must_define += vector_primer
vector_primer_help = file containt vector primer data

moa_must_define += cloning_vector
cloning_vector_help = File containing the cloning vector
 
moa_must_define += sequencing_vector
sequencing_vector_help = File containing the sequencing vector

moa_must_define += ecoli_screenseq
ecoli_screenseq_help = File containing ecoli screen sequences

moa_must_define += repeat_masker_lib
repeat_masker_lib_help = File with a repeatmasker library

moa_may_define += quality_value_clip
quality_value_clip_help = quality cutoff


#Include base moa code - does variable checks & generates help
ifneq $(include_moa_base) "no"
	include $(shell echo $$MOABASE)/template/moaBase.mk
endif

################################################################################

input_dirs = $(shell find $(input_dir) -name "$(input_pattern)" -type d)

pregap: pregap_prepare pregap_run

pregap_prepare:
	@echo $(input_dirs)
	
pregap_run:
	

#CLEAN	        
clean: pregap_clean
pregap_clean:
	@echo "TODO: Run clean"
		