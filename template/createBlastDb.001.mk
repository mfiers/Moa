# Create a BLAST database from a set of sequences
################################################################################

################################################################################
# Definitions

# Help
moa_ids += createBlastDb
moa_title_createBlastDb = Create a BLAST database 
moa_description_createBlastDb = Takes a multi-fasta input file and creates a BLAST database.

#Targets (for generating help)
moa_targets += 
createBlastDb_help = Create the BLAST database
clean_help = Remove the blast database
set_weka_help = set location in the global weka db
clean_weka_help = clean location in the global weka db (will not run automatically)

moa_must_define += bdb_name
bdb_name_help = Database name to create

moa_may_define += bdb_input_dir bdb_input_extension 
bdb_input_dir_help = Dir with the input fasta files, defaults to ./fasta
bdb_input_extension_help = extension of the input sequence files, defaults to fasta

#Variable: protein
moa_may_define += bdb_protein 
bdb_protein_help = Protein database? (T)rue) or not (F)alse (default: F)

#Include base moa code - does variable checks & generates help
include $(shell echo $$MOABASE)/template/moaBase.mk

# End of the generic part - from here on you're on your own :)

moa_register_extra += blastdb fastafile idlist
moa_register_blastdb = $(shell echo `pwd`/$(bdb_name))
moa_register_fastafile = $(shell echo `pwd`/$(bdb_name)).fasta
moa_register_idlist = $(shell echo `pwd`/$(bdb_name).list)

bdb_input_dir ?= ./fasta
bdb_input_extension ?= fasta


#the rest of the variable definitions 
bdb_protein ?= F
input_files ?= $(wildcard $(bdb_input_dir)/*.$(bdb_input_extension))
fasta_file = $(bdb_name).fasta

ifeq ("$(bdb_protein)", "F")
	one_blast_db_file = $(bdb_name).nhr
else
	one_blast_db_file = $(bdb_name).phr
endif

.PHONY: createBlastDb_prepare
createBlastDb_prepare:

.PHONY: createBlastDb_post
createBlastDb_post: create_id_list
	weka -r set $(bdb_name)::blastdb `pwd`/$(bdb_name)
	weka -r set $(bdb_name)::fasta `pwd`/$(input_file)
	weka -r set $(bdb_name)::idlist `pwd`/$(bdb_name)

.PHONY: createBlastDb
createBlastDb: $(one_blast_db_file)

$(one_blast_db_file): $(fasta_file)
	@echo "Creating $@"
	formatdb -i $< -p $(bdb_protein) -o T -n $(bdb_name)

$(fasta_file): $(input_files)
	-rm -f $(fasta_file)
	@for x in $^; do \
		cat $$x >> $(fasta_file) ;\
		echo >> $(fasta_file) ;\
	done

.PHONY: create_id_list
create_id_list: $(bdb_name).list

$(bdb_name).list: $(fasta_file)
	grep ">" $(fasta_file) | cut -c2- | sed 's/ /\t/' | sort > $(bdb_name).list

createBlastDb_clean:	
	-if [ $(bdb_protein) == "F" ]; then \
		rm $(bdb_name).n?? ;\
	else \
		rm $(bdb_name).p?? ;\
	fi
	-rm $(fasta_file)
	-rm $(bdb_name).list
	-rm formatdb.log

