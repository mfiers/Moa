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

moa_title = Glimmer3

moa_description = Predicts (prokaryotic) using glimmer3.

moa_ids += glimmer3

glimmer3_help = Glimmer3 is a open reading frame discovery program		\
  from the EMBOSS [[emboss]] package. It takes a set of input			\
  sequences and predicts all open reading frames. Additionally, this	\
  template converts the default output (predicted protein sequences)	\
  to GFF3.


#########################################################################
# Prerequisite testing

prereqlist += prereq_glimmer3_installed

prereq_glimmer3_installed:
	@if ! which glimmer3 >/dev/null; then \
		echo "glimmer3 is either not installed or not in your \$$PATH" ;\
		false ;\
	fi


moa_must_define += glimmer3_input_dir
blast_input_dir_help = directory containing the input sequences

moa_may_define +=  glimmer3_gff_source
blast_gff_source_help = source field to use in the gff. Defaults to "moa"

moa_may_define += glimmer3_input_extension
input_extension_help = input file extension. Defaults to 'fasta'

moa_may_define += glimmer3_runname

#preparing for possible gbrowse upload:
gup_gff_dir = ./gff
gup_upload_gff = T
gup_gffsource ?= $(blast_gff_source)

#include moabase, if it isn't already done yet..
include $(shell echo $$MOABASE)/template/moaBase.mk

glimmer3_runname ?= moa
glimmer3_gff_source ?= moa
glimmer3_input_extension ?= fasta

glimmer3_input_files ?= $(wildcard $(glimmer3_input_dir)/*.$(glimmer3_input_extension))

glimmer3_output_files = $(addprefix out/, $(notdir $(patsubst		\
    %.$(glimmer3_input_extension), %.predict, $(glimmer3_input_files))))

glimmer3_cds_files = $(addprefix out/, $(notdir $(patsubst		\
    %.$(glimmer3_input_extension), %.cds.fasta, $(glimmer3_input_files))))

#glimmer3_gff_files = $(addprefix gff/, \
#	$(patsubst %.orf, %.gff, $(notdir $(glimmer3_output_files))))

glimmer3_test:
	@echo "Input extension: '$(glimmer3_input_extension)'"
	@echo "a blastdb file: '$(single_glimmer3_db_file)'"
	@echo "No inp files $(words $(glimmer3_input_files))"
	@echo "No orf files $(words $(glimmer3_output_files))"
	@echo "No gff files $(words $(glimmer3_gff_files))"

#prepare for glimmer3 - i.e. create directories
.PHONY: glimmer3_prepare
glimmer3_prepare:	
	-mkdir out 
	-mkdir gff  
	-mkdir train
	-mkdir fasta

.PHONY: glimmer3_post
glimmer3_post:

glimmer3_clean:
	-rm -rf ./gff/
	-rm -rf ./train/
	-rm -rf ./out/
	-rm -rf ./fasta/


glimmer3_input_files ?= $(wildcard $(glimmer3_input_dir)/*.$(glimmer3_input_extension))

.PHONY: glimmer3
glimmer3: train/train.icm $(glimmer3_cds_files)

$(glimmer3_cds_files): out/%.cds.fasta: $(glimmer3_input_dir)/%.$(glimmer3_input_extension) out/%.predict
	extract -t $(realpath $<) $(realpath $(word 2,$^)) \
		| sed "s/orf\([0-9]*\)/$*.g3.g\1/" > $@
	fastaSplitter -f $@ -o fasta

$(glimmer3_output_files): out/%.predict: $(glimmer3_input_dir)/%.$(glimmer3_input_extension) train/train.icm
	cd out; \
		glimmer3 -o50 -g110 -t30 $(realpath $<) 					\
			$(realpath $@) ../train/train.icm $*; 					\


train/train.icm: train/train.set
	build-icm -r $@ < $<

train/train.set: train/longorfs train/all.seq
	extract -t train/all.seq $< > $@

train/longorfs: train/all.seq
	long-orfs -n -t 1.15 $< $@

train/all.seq: $(glimmer3_input_files)
	-rm fasta_in/all.seq
	for x in $^; do 												\
		cat $$x >> $@;												\
	done