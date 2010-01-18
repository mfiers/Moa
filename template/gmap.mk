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
moa_ids += gmap

moa_title_gmap = Gmap
moa_description_gmap = Run GMAP on an set of input files (query) \
  vs a database index.

#variables
moa_must_define += gmap_db
gmap_db_help = Gmap db
gmap_db_type = file

moa_must_define += gmap_input_file
gmap_input_file_help = input file with the sequences to map
gmap_input_file_type = file

moa_may_define += gmap_extra_parameters
gmap_extra_parameters_default = 
gmap_extra_parameters_help = extra parameters to feed to gmap
gmap_extra_parameters_type = string

moa_may_define += gmap_invert_gff
gmap_invert_gff_default = F
gmap_invert_gff_help = Invert the GFF (T/*F*)
gmap_invert_gff_type = set

gmap_invert_gff_allowed = T F
moa_may_define += gmap_gff_source
gmap_gff_source_default = gmap
gmap_gff_source_help = Source field to use in the output GFF
gmap_gff_source_type = string

ifndef dont_include_moabase
	include $(shell echo $$MOABASE)/template/moaBase.mk
endif

##### Derived variables for this run

#prepare for gbrowse updload
gup_gff_dir=.
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
		| sed "s/$(gmap_dbname)/$(gmap_gff_source)/" \
		| sed "s/cDNA_match/match/" \
		| sed "s/^\([^\t]*\)\(.*\)ID=\([^;]*\).path\([0-9]\+\);Name=\([^;]*\)\(.*\)/\1\2ID=gmap__\1__\3__\4;Name=gmap__\1__\3__\4\6/" \
		| sed "s/Target=/Target=Sequence:/" \
		> output.gff
	if [ "$(gmap_invert_gff)" == "T" ]; then \
		invertGff output.gff > output.invert.gff ;\
	fi

output.raw: $(gmap_input_file)
	gmap -D $(shell dirname $(gmap_db)) \
		 -d $(shell basename $(gmap_db)) \
		 $(gmap_extra_parameters) \
		 -A $< -F -f 3 > $@
	gmap -D $(shell dirname $(gmap_db)) \
		 -d $(shell basename $(gmap_db)) \
		 $(gmap_extra_parameters) \
		 $< -A -F -i 10 > output.align

gmap_clean:
	-rm -f output.gff
	-rm -f output.raw

