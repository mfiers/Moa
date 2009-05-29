# lftp a set of files

# Main target - should be first in the file
moa_main_target: check fasta2gff

################################################################################
# Definitions
# targets that the enduser might want to use
moa_targets += fasta2gff clean 
fasta2gff_help = generate gff from a fasta file
clean_help = Clean up. 

# Help
moa_ids += fasta2gff
moa_title_fasta2gff = Fasta to gff
moa_description_fasta2gff = Create gff from a fasta file to accompany upload to \
  a gbrowse db

# Output definition
moa_outputs += fasta2gff
moa_output_fasta2gff = ./gff/*
moa_output_fasta2gff_help = gff output files

#varables that NEED to be defined
moa_must_define += gffsource
gffsource_help = Source to be used in the gff

#varables that MAY  be defined
moa_may_define += input_dir 
input_dir_help = Directory with the input fasta (default: ./fasta)

moa_may_define += input_pattern
input_pattern_help = glob pattern of the fasta files (default: *.fasta) 

moa_may_define += fasta2gffoptions
fasta2gffoptions_help = options to be passed to the fasta2gff script 

#Include base moa code - does variable checks & generates help
ifndef dont_include_moabase
	include $(shell echo $$MOABASE)/template/moaBase.mk
endif

################################################################################

fasta2gffoptions?=
input_dir ?= ./fasta
input_pattern ?= *.fasta
input_files = $(wildcard $(input_dir)/$(input_pattern))
output_files = $(addprefix ./gff/, $(addsuffix .gff, $(notdir $(input_files))))

.PHONY: prep concat fasta2gff fasta2gff_run fasta2gff_prep

fasta2gff: fasta2gff_prep fasta2gff_run 
	
fasta2gff_prep:
	-mkdir gff
	
fasta2gff_run: $(output_files)
	@echo Run done

$(output_files): gff/%.gff : $(input_dir)/%
	fasta2gff $< -s $(gffsource) $(fasta2gffoptions) > $@

fasta/%.$(input_extension): $(input_dir)/%.$(input_extension)
	cat $< | sed '$(sed_command)' > $@ 
	
#CLEAN	        
clean: fasta2gff_clean
fasta2gff_clean:
	-rm -rf gff	