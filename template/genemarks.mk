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

moa_title = geneMarkS
moa_description = predict genes using geneMarkS 
moa_ids += genemarks
moa_genemarks_help = Predict genes using geneMarkS

moa_must_define += genemarks_input_dir
genemarks_input_dir_help = directory containing the input sequences
genemarks_input_dir_type = directory

moa_must_define += genemarks_matrix
genemarks_matrix_help = the matrix to use
genemarks_matrix_type = file

moa_may_define += genemarks_gff_source
genemarks_gff_source_default = genemarks
genemarks_gff_source_help = source field to use in the gff. Defaults to "geneMarkS"
genemarks_gff_source_type = string

moa_may_define += genemarks_input_extension
genemarks_input_extension_default = fasta
genemarks_input_extension_help = input file extension. Defaults to 'fasta'
genemarks_input_extension_type = string

#include moabase, if it isn't already done yet..
include $(shell echo $$MOABASE)/template/moaBase.mk

#define resultfilesets
genemarks_input_files = $(wildcard $(genemarks_input_dir)/*.$(genemarks_input_extension))

genemarks_out_files = $(addprefix out/, 										\
		$(notdir $(patsubst %.$(genemarks_input_extension), %.lst, 				\
		$(genemarks_input_files))))

genemarks_gff_files = $(addprefix gff/, 										\
		$(notdir $(patsubst %.$(genemarks_input_extension), %.gff, 				\
		$(genemarks_input_files))))

genemarks_cds_files = $(addprefix cds/, 										\
		$(notdir $(patsubst %.$(genemarks_input_extension), %.cds.fasta, 		\
		$(genemarks_input_files))))

genemarks: $(genemarks_gff_files) $(genemarks_cds_files)
	@echo "Created $(genemarks_gff_files)"
	@echo "Via $(genemarks_out_files)"
	@echo "From $(genemarks_input_files)"
	@echo "again $(genemarks_input_dir)/*.$(genemarks_input_extension)"

$(genemarks_gff_files): gff/%.gff: out/%.lst

$(genemarks_cds_files): cds/%.cds.fasta: out/%.orf
	cat $< 											\
		| grep -v '^;'								\
		| sed "s/orf_\([0-9]*\)/$*.gms.g\1/" 		\
		> $@

$(genemarks_out_files): out/%.lst: $(genemarks_input_dir)/%.$(genemarks_input_extension)
	@echo "working from $< to create $@"
	cd out; 														\
		ln -s  $(realpath $<) $*;									\
		gm -m $(genemarks_matrix) -onq -v $*							\

PHONY: genemarks_prepare
genemarks_prepare:
	-mkdir out
	-mkdir cds
	-mkdir fasta
	-mkdir gff

PHONY: genemarks_post
genemarks_post:

PHONY: genemarks_clean
genemarks_clean:
	-rm -rf fasta/
	-rm -rf cds/
	-rm -rf gff/
	-rm -rf out/
