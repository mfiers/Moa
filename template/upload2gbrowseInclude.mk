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
moa_targets += upload
upload_help = upload all new data to gbrowse

moa_may_define += gbrowse_user gbrowse_db
gbrowse_user_help = gbrowse db user. If not defined, this defaults to 'moa'.
gbrowse_db_help = gbrowse database. If not defined, this defaults to 'moa'.

moa_may_define += gbrowse_do_upload
gbrowse_do_upload_help = (T/F) Unless this value is T, the data will not be uploaded \
  to a gbrowse database

-include $(shell echo $$MOABASE)/template/moaBase.mk

gup_input_files = $(wildcard $(gup_input_dir)/*.$(gup_input_extension))
#gup_touch_files = $(addprefix upload/, $(notdir $(wildcard $(gup_input_dir)/*.$(gup_input_extension))))

gbrowse_user ?= moa
gbrowse_db ?= moa
gbrowse_do_upload ?= F

# function to delete the results of one, a few and all input files
# if sticking to a few rules this should work for most analyses.
gup_delete_single ?= bp_seqfeature_delete.pl -d $(gbrowse_db) -u $(gbrowse_user) \
  -n $(gff_source)_`basename $< .gff`
gup_delete_few ?= bp_seqfeature_delete.pl -d $(gbrowse_db) -u $(gbrowse_user) \
  -n $(addprefix $(gff_source)_, $(shell for f in $?; do basename $$f .$(gup_input_extension); done))
#gup_delete_all ?= bp_seqfeature_delete.pl -d $(gbrowse_db) -u $(gbrowse_user) \
#  -n $(addprefix $(gff_source)_, $(shell for f in $(gup_input_files); do basename $$f .$(gup_input_extension); done))
gup_delete_all ?= bp_seqfeature_delete.pl -d $(gbrowse_db) -u $(gbrowse_user) \
  -t '*:$(gff_source)'

# the default upload target runs make upload. This is to make sure that possible files
# created by the rest of this makefile are read correctly. I'm under the impression
# that this should be possible by secondary expanssion. but could not get this to
# work properly. If anybody has a bright idea.. please.

.PHONY: upload2gbrowse_prepare
upload2gbrowse_prepare: 

.PHONY: upload2gbrowse
upload2gbrowse:
	if [ "$(gbrowse_do_upload)" == "T" ]; then \
		$(MAKE) upload ;\
	fi

.PHONY: upload2gbrowse_post
upload2gbrowse_post: 

## Do the real upload
.NOTPARALLEL: upload
upload: $(gup_input_files)
	@echo "Uploading $(words $?) files"
	@echo $(gup_delete_few)
	$(gup_delete_few)
	bp_seqfeature_load.pl -d $(gbrowse_db) -u $(gbrowse_user) -f $?
	touch upload

.PHONY: upload2gbrowse_clean
upload2gbrowse_clean:
	@echo "Run upload2gbrowse_clean"
	-rm -r upload
	@echo "Executing $(gup_delete_all)"
	@echo -e "$(warn_on)Problem$(warn_off) - Not sure if bioperl is buggy here"
	@echo -e "$(warn_on)Problem$(warn_off) - features might not have been deleted from the db"
	$(delete_all_function)

