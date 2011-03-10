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

moa_id = glimmer3

#preparing for possible gbrowse upload:
gup_gff_dir = ./gff
gup_upload_gff = T
gup_gffsource ?= $(blast_gff_source)

#check if we have the ubuntu package installed - if so, prefix all commands
#with tigr-glimmer
ifeq ($(shell which tigr-glimmer 2>&1 || true),)
exec_prefix=tigr_glimmer
else
exec_prefix=
endif

#########################################################################
# Prerequisite testing

prereqlist += prereq_glimmer3_installed prereq_elph_installed \
			prereq_awkscripts_installed

prereq_glimmer3_installed:
	$(if exec_prefix,,@$(call checkPrereqPath,glimmer3))

prereq_elph_installed:
	@$(call checkPrereqPath,elph,You can download elph from						\
				 http://www.cbcb.umd.edu/software/ELPH/)

prereq_awkscripts_installed:
	@$(call checkPrereqPath,get-motif-counts.awk,Make sure you copied the 		\
			glimmer3 AWK scripts into your PATH)
	@$(call checkPrereqExec,get-motif-counts.awk --version,						\
			Check the AWK shebang!)

#include moabase, if it isn't already done yet..
include $(MOABASE)/lib/gnumake/core.mk
glimmer3_input_files ?= $(wildcard $(glimmer3_input_dir)/*.$(glimmer3_input_extension))
glimmer3_output_files = $(addprefix out/, $(notdir $(patsubst		\
    %.$(glimmer3_input_extension), %.g3.predict, $(glimmer3_input_files))))

glimmer3_cds_files = $(addprefix out/, $(notdir $(patsubst		\
    %.$(glimmer3_input_extension), %.g3.cds.fasta, $(glimmer3_input_files))))

glimmer3_gff_files = $(addprefix gff/, $(notdir $(patsubst		\
    %.$(glimmer3_input_extension), %.g3.gff, $(glimmer3_input_files))))

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

.PHONY: glimmer3
glimmer3: glimmer3_prepare $(glimmer3_gff_files) $(glimmer3_cds_files)

$(glimmer3_gff_files): gff/%.g3.gff: out/%.g3.predict
	cat $<											\
		| grep -v "^>"								\
		| sed "s/orf\([0-9]*\)/$*.g3.g\1/" 			\
		| awk ' {																	\
					printf "$*\t$(glimmer3_gff_source)\tCDS\t";						\
					if ($$4 > 0) { 													\
						printf "%s\t%s\t%s\t+\t%s", $$2, $$3, $$5, substr($$4,2,1); } 			\
					else { 															\
						printf "%s\t%s\t%s\t-\t%s", $$3, $$2, $$5, substr($$4,2,1); } 			\
					printf "\tID=%s;Name=%s\n", $$1, $$1;							\
				} ' 																\
		> $@

$(glimmer3_cds_files): out/%.g3.cds.fasta: \
		$(glimmer3_input_dir)/%.$(glimmer3_input_extension) out/%.g3.predict
	cat $(realpath $(word 2,$^)) 					\
		| grep -v "^>"								\
		| extract -t $(realpath $<) -				\
		| sed "s/orf\([0-9]*\)/$*.g3.g\1/" 			\
		> $@
	fastaSplitter -f $@ -o fasta

$(glimmer3_output_files): out/%.g3.predict: 									\
		$(glimmer3_input_dir)/%.$(glimmer3_input_extension) 					\
		train/upstream.motif train/train1.icm
	startuse=`start-codon-distrib -3 train/all.seq train/run1.coords`;			\
	cd out; 																	\
		glimmer3 																\
			-o$(glimmer3_max_overlap) 											\
			-g$(glimmer3_gene_len)												\
			-t$(glimmer3_treshold)												\
			-b ../train/upstream.motif											\
			-P $$startuse														\
			$(realpath $<) 														\
			../train/train1.icm $*.g3

#run elph to create analyze motifs
train/upstream.motif: train/upstream.train.set
	elph $< LEN=6 | get-motif-counts.awk > $@

#create an upstream set
train/upstream.train.set: train/run1.coords train/all.seq
	upstream-coords.awk 25 0 $< | extract train/all.seq - > $@

#get the coordinates of the predicted seqs from the first glimmer run
train/run1.coords: train/run1.predict
	cat $< | grep -v "^>" > $@

#do the first glimmer run, based on the simple training set
train/run1.predict: train/train1.icm
	cd train; glimmer3 													\
		-o$(glimmer3_max_overlap) -g$(glimmer3_gene_len)				\
		-t$(glimmer3_treshold) 											\
		all.seq train1.icm run1

#build the training model
train/train1.icm: train/train1.set
	build-icm -r $@ < $<

#create a training set from all ORFs
train/train1.set: train/all.seq train/long.orfs 
	extract -t $^ > $@

#assume a linear genome - circular would not make sense with
#possibly multiple genomes concatenated 
train/long.orfs: train/all.seq
	long-orfs -l -n -t 1.15 $< $@

#concatenate all seqs into one - this is only for training!!
train/all.seq: $(glimmer3_input_files)
	echo ">train" > $@
	for x in $^; do 												\
		cat $$x | grep -v "^>"  >> $@;								\
	done