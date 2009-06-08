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
moa_description_upload2gbrowse = Upload data to a seqfeature gbrowse database

################################################################################
## Definitions
## targets that the enduser might want to use
moa_targets += gbrowse_upload gbrowse_clean
gbrowse_upload_help = Upload data to gbrowse
gbrowse_clean = clean all datat from this analysis from the gbrowse database
moa_must_define += gbrowse_user gbrowse_db
gbrowse_user_help = gbrowse db user
gbrowse_db_help = gbrowse database

## Define functions to determine id & source - helps in deleting stuff from the db 
## Not sure if we really need this!
get_id ?= basename $$file .$(input_extension)
get_source ?= echo $(gff_source)

upload_touch_files = $(addprefix upload/, $(notdir $(gbrowse_upload_files)))

#define the functions to actually delete the stuff. I don't think these will need
#to be overidden very often, but, at least it is possible now.
delete_function ?= bp_seqfeature_delete.pl -d $(gbrowse_db) -u $(gbrowse_user) -n $$id
delete_all_function ?= bp_seqfeature_delete.pl -d $(gbrowse_db) -u $(gbrowse_user) -t '$$method:$$source'

gup_input_files = $(wildcard $(gup_input_dir)/*.$(gup_input_extension))
gup_touch_files = $(addprefix upload/, $(notdir $(gup_input_files)))

## Shortcut for gbrowse_upload.. which is way too long
.PHONY: upl
upl: gbrowse_upload

.PHONY: gbrowse_upload
gbrowse_upload: gbrowse_upload_prepare $(gup_touch_files) gbrowse_batch_upload
	@echo "finish gbrowse_upload"

.PHONY: gbrowse_batch_upload
gbrowse_batch_upload: $(gup_input_files)
	@echo all $^
	@echo new $?
	echo "uploading $?"
	bp_seqfeature_load.pl -d $(gbrowse_db) -u $(gbrowse_user) -f $?
	touch gbrowse_batch_upload

gbrowse_upload_prepare:
	-mkdir upload# remaking the touch file - thus the gff file is either newer than the touch
# file or the touch file does not exist yet. In the latter case, just create
# the touch file else, delete data from the db.
upload/%: $(gup_input_dir)/%
	echo "Looking at : $@ and $<"
	@if [[ -f "$@" ]]; then \
		echo "deleting gbrowse data for $<" ;\
			echo Execution: $(gup_delete_single_f) ;\
			$(gup_delete_single) ;\
	fi
	touch $@gbrowse_upload_clean:
	-rm -rf upload


status_upload2gbrowse:
	@echo "Gbrowse upload status"
	@echo "Files to upload: $(words $(gbrowse_upload_files))"
	@echo "First file to upload: $(word 1, $(gbrowse_upload_files))"

