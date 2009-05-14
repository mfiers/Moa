# lftp a set of files

# Main target - should be first in the file
moa_main_target: check clean_fasta

################################################################################
# Definitions
# targets that the enduser might want to use
moa_targets += clean_fasta clean
clean_fasta_help = Cleanup of FASTA files
clean_help = Remove anything that is not called Makefile or moa.mk 

# Help
moa_title = clean Fasta
moa_description = Convert files to unix format and convert all characters \
 that are not an A,C,G,T or N to N. 

# Output definition
moa_outputs += clean_fasta
moa_output_clean_fasta = ./fasta/*.fasta
moa_output_clean_fasta_help = Cleaned fasta files

#varables that NEED to be defined
moa_must_define += input_dir
input_dir_help = list of directories with the input files

moa_may_define += input_extension sed_command
input_extension_help = extension to the fasta files (default .fasta)
sed_command_help = The sed command cleaning the code, defaults to \
  '/^>/!s/[^ACGTNacgtn]/N/g'
#Include base moa code - does variable checks & generates help				 
include $(shell echo $$MOABASE)/template/moaBase.mk

################################################################################

#output_files = $(add_prefix fasta/, $(notdir $(wildcard $(input_dir)/*.$(input_extension)))))
output_files = $(addprefix fasta/, $(notdir $(wildcard $(input_dir)/*.$(input_extension))))
input_extension ?= fasta
clean_fasta: clean_fasta_prep clean_fasta_run
sed_command ?= /^>/!s/[^ACGTNacgtn]/N/g

clean_fasta_prep:
	-mkdir fasta		
	
clean_fasta_run: $(output_files)

fasta/%.$(input_extension): $(input_dir)/%.$(input_extension)
	cat $< | sed '$(sed_command)' > $@ 
	        
#Clean	
clean: clean_fasta_clean

clean_fasta_clean:
	-rm -rf fasta	