#
# upload to gbrowse, only used as an extension to an analysis
# i.e. should be included by another makefile
#
# The embedding makefile should define what needs to be 
# uploaded, i.e. a list of fasta / gff files
# this goes in the variale gbrowse_upload_files
#
moa_ids += upload2gbrowse
moa_title_upload2gbrowse = Upload to gbrowse
moa_description_upload2gbrowse = Upload data to a seqfeature gbrowse database################################################################################
# Definitions
# targets that the enduser might want to use
moa_targets += gbrowse_upload gbrowse_clean
gbrowse_upload_help = Upload data to gbrowse
gbrowse_clean = clean all datat from this analysis from the gbrowse databasemoa_must_define += gbrowse_user gbrowse_db
gbrowse_user_help = gbrowse db user
gbrowse_db_help = gbrowse database
#define functions to determine id & source - helps in deleting stuff from the db 
get_id ?= basename $$file .$(input_extension)
get_source ?= echo $(gff_source)

#define the functions to actaull delete the stuff. I don't think these will need
#to be overidden very often, but, at least it is possible now.
delete_function ?= bp_seqfeature_delete.pl -d $(gbrowse_db) -u $(gbrowse_user) -n $$id
delete_all_function ?= bp_seqfeature_delete.pl -d $(gbrowse_db) -u $(gbrowse_user) -t '$$method:$$source'gbrowse_upload: $(gbrowse_upload_files)
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
	touch gbrowse_uploadgbrowse_clean:
	-rm gbrowse_upload