# 
# Copyright 2009 Mark Fiers, Plant & Food Research
# 
# This file is part of Moa - http://github.com/mfiers/Moa
# 
# Moa is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your
# option) any later version.
# 
# Moa is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
# License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Moa.  If not, see <http://www.gnu.org/licenses/>.
# 
moa_title = Library for uploading data to GBrowse
moa_description = A library that aids in uploading FASTA and GFF		\
  to a Generic Genome Browser database. This template is only to be		\
  used embedded in another template. This library expects that the		\
  following variables are preset; gup_fasta_dir, gup_gff_dir, gffsource	\
  gup_upload_fasta, gup_upload_gff

moa_ids += upload2gbrowse
moa_upload2gbrowse_help = Upload to gbrowse

moa_additional_targets += initGbrowse gupgo
moa_initGbrowse_help = Clean & initalize a gbrowse database. 			\
	**Warning: all data will be lost!**
moa_gupgo_help = Actually do the upload. upload2gbrowse NEVER does	\
	this automatically!

moa_must_define += gup_user gup_db gup_gffsource 
gup_user_help = gbrowse db user. If not defined, this defaults to 'moa'.
gup_db_help = gbrowse database. If not defined, this defaults to 'moa'.
gup_gffsource_help = the gff source field, used in batch operations

moa_may_define += gup_gff_extension gup_fasta_extension
gup_fasta_extension_help = extension of the FASTA files to upload (.fasta)
gup_gff_extension_help = extension of the GFF files to upload (.gff)

moa_may_define += gup_upload_fasta gup_upload_gff gup_force_upload
gup_upload_fasta_help = upload fasta to gbrowse (T/F)
gup_upload_gff_help = upload gff to gbrowse (T/F)
gup_force_upload_help = upload to gbrowse, ignore gup_lock and upload	\
  all, not only files newer that upload_gff or upload_fasta

moa_may_define += marks_extensions
marks_extensions_help = Add some extensions to the Gbrowse database to \
  be initalized, for use by Mark.

include $(shell echo $$MOABASE)/template/moaBase.mk

gup_gff_extension ?= gff
gup_fasta_extension ?= fasta
gup_gff_dir ?= ./gff
gup_fasta_dir ?= ./fasta

#Per default we're not uploading. you really need to set this.
gup_upload_fasta ?= F
gup_upload_gff ?= F

marks_extensions ?= F

#see if this job is locked from uploading
gup_locked = $(shell if [ -f ./gup_lock ]; then echo "T"; else echo "F"; fi)

# the default upload target runs make upload. This is to make sure
# that possible files created by the rest of this makefile are read
# correctly. I'm under the impression that this should be possible by
# secondary expanssion. but could not get this to work properly. If
# anybody has a bright idea.. please.

.PHONY: upload2gbrowse_prepare
upload2gbrowse_prepare: 

## We never ever go through automatic invocation!
## This is too complicated. Needs to be called with
## "make gup_up"
## or 
## "make all action="gup_up""
.PHONY: upload2gbrowse
upload2gbrowse:

.PHONY: upload2gbrowse_post
upload2gbrowse_post: 

## Do the actual upload
.PHONY: gupgo
gupgo: $(if ifeq("$(gup_upload_fasta)", "T"), gup_do_fasta_upload) \
		$(if ifeq("$(gup_upload_gff)", "T"), gup_do_gff_upload)
	@echo "finished gbrowse upload"

.PHONY: gup_do_fasta_upload gup_do_gff_upload 
gup_do_fasta_upload: 
	@$(call echo,Start FASTA upload)
	@find $(gup_fasta_dir) -name "*.$(gup_fasta_extension)" 					\
		| xargs -n 200 bp_seqfeature_load.pl 									\
				-d $(gup_db) -u $(gup_user) -f
	@$(call echo,Finished FASTA upload)

gup_do_gff_upload: 
	@$(call echo,Start GFF upload)
	@find $(gup_gff_dir) -name "*.$(gup_gff_extension)"							\
		| xargs -n 200 bp_seqfeature_load.pl 									\
				-d $(gup_db) -u $(gup_user) -f
	@$(call echo,Finished GFF upload)

##
## initGbrowse functionality
##

initGbrowse: mark_add_1 = 									\
	ALTER TABLE $(gup_db).name								\
	ADD COLUMN `pid` int(10) NOT NULL AUTO_INCREMENT,		\
	ADD PRIMARY KEY (`pid`)

initGbrowse: mark_add_2 =									\
	ALTER TABLE $(gup_db).attribute 						\
	ADD COLUMN `pid` int(10) NOT NULL AUTO_INCREMENT, 		\
	ADD PRIMARY KEY (`pid`)

initGbrowse: mark_add_3 = 									\
	ALTER TABLE $(gup_db).parent2child						\
	ADD COLUMN `pid` int(10) NOT NULL AUTO_INCREMENT, 		\
	ADD PRIMARY KEY (`pid`)

initGbrowse:
	bp_seqfeature_load.pl -d $(gup_db) -u $(gup_user) -c
	if [ "$(marks_extensions)" == "T" ]; then 				\
		mysql -u$(gup_user) -e '$(mark_add_1)';				\
		mysql -u$(gup_user) -e '$(mark_add_2)';				\
		mysql -u$(gup_user) -e '$(mark_add_3)';				\
	fi
	touch lock



