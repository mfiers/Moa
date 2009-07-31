#
#    Copyright 2009 Mark Fiers
#
#    This file is part of Moa 
#
#    Moa is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Moa is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Moa.  If not, see <http://www.gnu.org/licenses/>.
#
#    See: http://github.com/mfiers/Moa/
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
moa_targets += upload
upload_help = upload all new data to gbrowse

moa_must_define += gup_user gup_db gup_gffsource
gup_user_help = gbrowse db user. If not defined, this defaults to 'moa'.
gup_db_help = gbrowse database. If not defined, this defaults to 'moa'.
gup_gffsource_help = the gff source field, used in batch operations

moa_may_define += gup_upload_fasta gup_upload_gff gbrowse_do_upload
gup_upload_gff_help = Perform gff upload (T/F)
gup_upload_fasta_help = Perform fasta upload (T/F)
gbrowse_do_upload_help = Deprecated: use gup_upload_gff or gup_upload_fasta

-include $(shell echo $$MOABASE)/template/moaBase.mk

gup_gff_extension ?= gff
gup_fasta_extension ?= fasta

gup_gff_dir ?= ./gff
gup_fasta_dir ?= ./fasta

gup_upload_fasta ?= F
gup_upload_gff ?= F

gup_input_gff = $(wildcard $(gup_gff_dir)/*.$(gup_gff_extension))
gup_input_fasta = $(wildcard $(gup_fasta_dir)/*.$(gup_fasta_extension))

# function to delete the results of one, a few and all input files
# if sticking to a few rules this should work for most analyses.
gup_delete_single ?= bp_seqfeature_delete.pl -d $(gup_db) \
  -u $(gup_user) -n $(gup_gffsource)_`basename $< .gff`

#delete a few files (file list in $?)
gup_delete_few ?= bp_seqfeature_delete.pl -d $(gup_db) \
  -u $(gup_user) \
  -n $(addsuffix *,\
       $(addprefix \
         $(gup_gffsource)_, \
         $(shell for f in $?; \
                   do basename $$f .$(gup_gff_extension); \
                 done) \
        ) \
      )

#delete all: Note, this will probably not work, the current version 
# of bp_seqfeature_delete.pl seems to be broken
gup_delete_all ?= bp_seqfeature_delete.pl -d $(gup_db) \
  -u $(gup_user) \
  -n $(gup_gffsource)_*

# the default upload target runs make upload. This is to make sure
# that possible files created by the rest of this makefile are read
# correctly. I'm under the impression that this should be possible by
# secondary expanssion. but could not get this to work properly. If
# anybody has a bright idea.. please.

.PHONY: upload2gbrowse_prepare
upload2gbrowse_prepare: 

.PHONY: upload2gbrowse
upload2gbrowse:
	@echo "new instance of make -> make sure that all created"
	@echo "files are actually recognized"
	$(MAKE) -j 1 upload2gbrowse2; 
	echo "End of make upload2gbrowse2"


.PHONY: upload2gbrowse_post
upload2gbrowse_post: 

## Do the actual upload
.PHONY: upload2gbrowse2
upload2gbrowse2: upload_fasta upload_gff
	@echo "finished with upload to gbrowse" 

upload_fasta: $(gup_input_fasta)
	if [ "$(gup_upload_fasta)" == "T" ]; then \
		echo "Uploading $(words $?) fasta files";\
		bp_seqfeature_load.pl -d $(gup_db) -u $(gup_user) -f $?;\
		touch upload_fasta;\
	fi

upload_gff: $(gup_input_gff) 
	if [ "$(gup_upload_gff)" == "T" ]; then \
		echo "Uploading $(words $?) gff files";\
		echo "deleting older stuff $(gup_delete_few)";\
		$(gup_delete_few);\
		bp_seqfeature_load.pl -d $(gup_db) -u $(gup_user) -f $?;\
		touch upload_gff;\
	fi

.PHONY: upload2gbrowse_clean
upload2gbrowse_clean: $(gup_input_gff)
	@echo "executing upload2gbrowse_clean" 
	$(gup_delete_all)
	-rm upload_gff
	-rm upload_fasta

