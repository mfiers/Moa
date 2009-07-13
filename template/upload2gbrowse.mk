################################################################################
# Use the include

moa_may_define += gup_fasta_dir gup_gff_dir gffsource
gup_fasta_dir_help = input directory with fasta files to upload to gbrowse
gup_gff_dir_help = input directory with gff files to upload to gbrowse
gffsource_help = gff "source" of the data to upload

gbrowse_do_upload = T
include $(shell echo $$MOABASE)/template/__upload2gbrowse.mk

