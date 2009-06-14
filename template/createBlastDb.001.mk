# Create a BLAST database from a set of sequences
################################################################################

################################################################################
# Definitions

# Help
moa_ids += createBlastDb
moa_title_createBlastDb = Create a BLAST database 
moa_description_createBlastDb = Takes a multi-fasta input file and creates a BLAST database.

#Targets (for generating help)
moa_targets += createBlastDb clean set_blastdb_weka clean_blastdb_weka
createBlastDb_help = Create the BLAST database
clean_help = Remove the blast database
set_weka_help = set location in the global weka db
clean_weka_help = clean location in the global weka db (will not run automatically)

#Outputs (for generating help)
moa_outputs += blastdb
moa_output_blastdb = ./set_name.???
moa_output_blastdb_help = The blast database created

#Variable: set_name
moa_must_define += name 
name_help = The name of the set, determines the name of the blast db

moa_may_define = input_dir input_extension
input_dir_help = Dir with the input fasta files, defaults to ./fasta
input_extension_help = extension of the input sequence files, defaults to fasta

#Variable: protein
moa_may_define += protein 
protein_help = Protein database? (T)rue) or not (F)alse (default: F)



#Include base moa code - does variable checks & generates help
include $(shell echo $$MOABASE)/template/moaBase.mk


# End of the generic part - from here on you're on your own :)

input_dir ?= ./fasta
input_extension ?= fasta


#the rest of the variable definitions 
protein ?= F
input_files ?= $(wildcard $(input_dir)/*.$(input_extension))
fasta_file = $(name).fasta

ifeq ("$(protein)", "F")
	one_blast_db_file = $(name).nhr
else
	one_blast_db_file = $(name).phr
endif

.PHONY: createBlastDb_prepare
createBlastDb_prepare:

.PHONY: createBlastDb_post
createBlastDb_post:

.PHONY: createBlastDb
createBlastDb: $(one_blast_db_file)

$(one_blast_db_file): $(fasta_file)
	@echo "Creating $@"
	formatdb -i $< -p $(protein) -o T -n $(name)

$(fasta_file): $(input_files)
	-rm -f $(fasta_file)
	for x in $^; do \
		cat $$x >> $(fasta_file) ;\
		echo >> $(fasta_file) ;\
	done

create_id_list: $(name).list

$(name).list: $(fasta_file)
	grep ">" $(fasta_file) | cut -c2- | sed 's/ /\t/' | sort > $(name).listset_blastdb_weka:
	weka -r set $(name)::blastdb `pwd`/$(name)
	weka -r set $(name)::fasta `pwd`/$(input_file)
	weka -r set $(name)::idlist `pwd`/$(name).listclean: createBlastDb_clean

createBlastDb_clean:	
	-if [ $(protein) == "F" ]; then \
		rm $(name).n?? ;\
	else \
		rm $(name).p?? ;\
	fi
	-rm $(fasta_file)
	-rm formatdb.log

clean_blastdb_weka:
	weka rm $(name)::blastdb