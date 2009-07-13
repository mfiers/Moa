# Create a BLAST database from a set of sequences
################################################################################

# Main target defintion
moa_main_target: check create_blast_db create_id_list set_blastdb_weka

################################################################################
# Definitions

# Help
moa_ids += createblastdb
moa_deprecated_createblastdb = Yes
moa_title_createblastdb = Create a BLAST database 
moa_description_createblastdb = Takes a multi-fasta input file and creates a BLAST database.

#Targets (for generating help)
moa_targets += create_blast_db clean set_blastdb_weka clean_blastdb_weka
create_blast_db_help = Create the BLAST database
clean_help = Remove the blast database
set_weka_help = set location in the global weka db
clean_weka_help = clean location in the global weka db (will not run automatically)

#Variable: set_name
moa_must_define += bdb_name bdb_input_file
bdb_name_help = The name of the set, determines the name of the blast db
bdb_input_file_help = Multifasta used as input. (default: $(name).fasta)

#Variable: protein
moa_may_define += bdb_protein 
bdb_protein_help = Protein database? (T)rue) or not (F)alse (default: F)

#Include base moa code - does variable checks & generates help
ifndef dont_include_moabase
	include $(shell echo $$MOABASE)/template/moaBase.mk
endif

################################################################################
# End of the generic part - from here on you're on your own :)

.PHONY: create_blast_db

#the rest of the variable definitions 
bdb_protein ?= F
bdb_input_file ?= $(bdb_name).fasta
ifeq ("$(bdb_protein)", "F")
	one_blast_db_file = $(bdb_name).nhr
else
	one_blast_db_file = $(bdb_name).phr
endif

.PHONY: create_blast_db_prepare
createblastdb_prepare:

createblastdb: $(one_blast_db_file)

$(one_blast_db_file): $(bdb_input_file)
	@echo "Creating $@"
	formatdb -i $< -p $(bdb_protein) -o T -n $(bdb_name)

create_id_list: $(bdb_name).list

$(bdb_name).list: $(bdb_input_file)
	grep ">" $< | cut -c2- | sed 's/ /\t/' | sort > $@

set_blastdb_weka:
	weka -r set $(bdb_name)::blastdb `pwd`/$(bdb_name)
	weka -r set $(bdb_name)::fasta `pwd`/$(bdb_input_file)
	weka -r set $(bdb_name)::idlist `pwd`/$(bdb_name).list	

clean: create_blast_db_clean
create_blast_db_clean:	
	-if [ $(bdb_protein) == "F" ]; then \
		rm $(bdb_name).n?? ;\
	else \
		rm $(bdb_name).p?? ;\
	fi

clean_blastdb_weka:
	weka rm $(bdb_name)::blastdb