# lftp a set of files

# Main target - should be first in the file
moa_main_target: check concatenate weka_set

################################################################################
# Definitions
# targets that the enduser might want to use
moa_targets += concatenate clean weka_set clean_weka
concatenate_help = Concatenate a set of FASTA files
weka_set_help = store this location in the weka variable db
clean_help = Clean up. 
clean_weka_help = clean location in the global weka db (will not run automatically)

# Help
moa_title = Concatenate
moa_description = Concatenate a set of fasta files into one.

# Output definition
moa_outputs += concatenate
moa_output_concatenate = ./outputfile.fasta
moa_output_concatenate_help = The concatenated file

#varables that NEED to be defined
moa_must_define += input_dir name
input_dir_help = Directory with the input data
name_help = name of the file, the outputfile will become ./name.fasta 

moa_may_define += input_extension
input_extension_help = extension to the fasta files (default .fasta)

#Include base moa code - does variable checks & generates help				 
include $(shell echo $$MOABASE)/template/moaBase.mk

################################################################################

input_extension ?= fasta
input_files = $(wildcard $(input_dir)/*.$(input_extension))
output_file = $(name).fasta

.PHONY: prep concat concatenate concatenate_run

concatenate: concatenate_run
	
concatenate_run: $(output_file)

$(output_file):  $(input_files) 
	-rm $(output_file)
	@cat $(input_files) > $(output_file)	
	@echo "end of concatenation"
	
fasta/%.$(input_extension): $(input_dir)/%.$(input_extension)
	cat $< | sed '$(sed_command)' > $@ 
	        
weka_set:
	weka set $(name)::fasta `pwd`/$(output_file)

clean_weka:
	weka rm $(name)::blastdb
	
#CLEAN	        
clean: concatenate_clean
concatenate_clean:
	-rm $(name).fasta	