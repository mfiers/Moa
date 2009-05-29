# lftp a set of files

# Main target - should be first in the file
moa_main_target: check upload2gbrowse

################################################################################
# Definitions
# targets that the enduser might want to use
moa_targets += upload2gbrowse clean
upload2gbrowse_help = Upload data to gbrowse

# Helpm
moa_ids += upload2gbrowse
moa_title_upload2gbrowse = Upload to gbrowse
moa_description_upload2gbrowse = Upload data to a seqfeature gbrowse database

#varables that NEED to be defined
moa_must_define += input_dir input_extension
input_dirs_help = Directories with the input data, either fasta or gff 
input_extension_help = filename extension to look for

moa_must_define += gbrowse_user gbrowse_db
gbrowse_user_help = gbrowse db user
gbrowse_db_help = gbrowse db 

moa_may_define += gbrowse_source gbrowse_method
gbrowse_source_help = Source of the gbrowes data
gbrowse_method_help = method of the gbrowse data 

#Include base moa code - does variable checks & generates help
ifndef dont_include_moabase
	include $(shell echo $$MOABASE)/template/moaBase.mk
endif

################################################################################

.PHONY: upload2gbrowse

input_files = $(wildcard $(input_dir)/*.$(input_extension))

get_id = basename $$file .$(input_extension)
get_source = echo 'PGSC.*'
get_method = echo 'Sequence'
delete_function=bp_seqfeature_delete.pl -d $(gbrowse_db) -u $(gbrowse_user) -n $$id
delete_all_function=bp_seqfeature_delete.pl -d $(gbrowse_db) -u $(gbrowse_user) -t '$$method:$$source'

upload2gbrowse: gbrowse_upload

gbrowse_upload: $(input_files)
	#predelete
	for file in $?; do \
		echo "deleting gbrowse data for $$file" ;\
		if [[ "$$file" =~ ".fasta$$" ]]; then \
			echo "Skipping delete, this appears to be a fasta file" ;\
		else \
			id=`$(get_id)` ;\
			source=`` ;\
			method=`` ;\
			echo Execution: $(delete_function) ;\
			$(delete_function) ;\
		fi ;\
	done	
	bp_seqfeature_load.pl -d $(gbrowse_db) -u $(gbrowse_user) -f $?
	touch gbrowse_upload
	
#CLEAN	        
clean: upload2gbrowse_clean

upload2gbrowse_clean:
	-rm gbrowse_upload
		