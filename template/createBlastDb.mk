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
moa_must_define += name input_file
name_help = The name of the set, determines the name of the blast db
input_file_help = Multifasta used as input. (default: $(name).fasta)

#Variable: protein
moa_may_define += protein 
protein_help = Protein database? (T)rue) or not (F)alse (default: F)

#Include base moa code - does variable checks & generates help
ifneq $(include_moa_base) "no"
	include $(shell echo $$MOABASE)/template/moaBase.mk
endif

################################################################################
# End of the generic part - from here on you're on your own :)

.PHONY: create_blast_db

#the rest of the variable definitions 
protein ?= F

ifeq ("$(protein)", "F")
	one_blast_db_file = $(name).nhr
else
	one_blast_db_file = $(name).phr
endif
     

create_blast_db: $(one_blast_db_file)

$(one_blast_db_file): $(input_file)
	@echo "Creating $@"
	formatdb -i $< -p $(protein) -o T -n $(name)

set_weka:
	weka set $(name)::blastdb `pwd`/$(name)
	
	
clean: create_blast_db_clean
create_blast_db_clean:	
	-if [ $(protein) == "F" ]; then \
		rm $(name).n?? ;\
	else \
		rm $(name).p?? ;\
	fi
	
clean_weka:
	weka rm $(name)::blastdb