# Run Gmap
################################################################################

# Variable checks & definition & help
moa_ids += gmap 
moa_title_gmap = Gmap
moa_description_gmap = Run GMAP on an set of input files (query) \
  vs a database index.

#variables
moa_must_define += gmap_db
gmap_db_help = Gmap db
gmap_db_cdbattr = gmapdb

moa_must_define += gmap_input_file
gmap_input_file_help = input file with the sequences to map
gmap_input_file_cdbattr = fastafile

moa_may_define += gmap_extra_parameters
gmap_extra_parameters_help = extra parameters to feed to gmap

ifndef dont_include_moabase
	include $(shell echo $$MOABASE)/template/moaBase.mk
endif

##### Derived variables for this run

gmap_dbname:=$(shell basename $(gmap_db))

#prepare for gbrowse updload
gup_gff_dir ?= .
gup_upload_gff?=T
gup_upload_fasta?=F
gup_gffsource?=gmap.$(gmap_dbname)


.PHONY: gmap_prepare
gmap_prepare:

.PHONY: gmap_post
gmap_post: 

.PHONY: gmap
gmap: output.gff

output.gff: output.raw
	cat output.raw \
		| sed "s/$(gmap_dbname)/gmap.$(gmap_dbname)/" \
		| sed "s/cDNA_match/match/" \
		| sed "s/^\([^\t]*\)\(.*\)ID=/\1\2ID=gmap.$(gmap_dbname)_\1_/" \
		| sed "s/Target=/Target=Sequence:/" \
		> output.gff

output.raw: $(gmap_input_file)
	gmap -D $(shell dirname $(gmap_db)) \
		 -d $(shell basename $(gmap_db)) \
		 $(gmap_extra_parameters) \
		 -A $< -f 3 > $@

gmap_clean:
	-rm -f output.gff
	-rm -f output.raw


