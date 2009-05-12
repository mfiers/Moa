# Create a BLAST database from a set of sequences
################################################################################

# Main target defintion
moa_main_target: check create_blast_db set_weka


################################################################################
# Definitions

# Help
moa_title = Create a BLAST database 
moa_description = Takes a multi-fasta input file and creates a BLAST database.

#Targets (for generating help)
moa_targets += create_blast_db clean set_weka clean_weka
create_blast_db_help = Create the BLAST database
clean_help = Remove the blast database
set_weka_help = set location in the global weka db
clean_weka_help = clean location in the global weka db (will not run automatically)

#Outputs (for generating help)
moa_outputs += blastdb
moa_output_blastdb = ./set_name
moa_output_blastdb_help = The blast database created

#Variable: set_name
moa_must_define += set_name 
set_name_help = The name of the set, determines the name of the blast db

#Variable: protein
moa_may_define += protein
protein_help = Protein database? (T)rue) or not (F)alse (default: F)

#Variable: input_file
moa_may_define += input_file 
input_file_help = Multifasta used as input. (default: $(set_name).fasta)

#Include base moa code - does variable checks & generates help				 
include $(shell echo $$MOABASE)/template/moaBase.mk
	
#the rest of the variable definitions 
protein ?= F
input_file	?= $(set_name).fasta

ifeq ("$(protein)", "F")
	one_blast_db_file = $(set_name).nhr
else
	one_blast_db_file = $(set_name).phr
endif
     
################################################################################
# End of the generic part - from here on you're on your own :)

.PHONY: create_blast_db

create_blast_db: $(one_blast_db_file)

$(one_blast_db_file): $(input_file)
	@echo "Creating $@"
	formatdb -i $< -p $(protein) -o T -n $(set_name)

set_weka:
	weka set $(set_name)::blastdb `pwd`/$(set_name)
	
clean: create_blast_db_clean

create_blast_db_clean:	
	-if [ $(protein) == "F" ]; then \
		rm $(set_name).n?? ;\
	else \
		rm $(set_name).p?? ;\
	fi
	
clean_weka:
	weka rm $(set_name)::blastdb