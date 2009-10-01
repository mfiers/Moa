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

moa_title = Getorf

moa_description = Predicts open reading frames using the EMBOSS	\
  [[emboss]] getorf tool.

moa_prerequisites += The [EMBOSS]() [[emboss]] suite of tools

moa_ids += getorf

moa_getorf_help = Getorf is a open reading frame discovery program		\
  from the EMBOSS [[emboss]] package. It takes a set of input			\
  sequences and predicts all open reading frames. Additionally, this	\
  template converts the default output (predicted protein sequences)	\
  to GFF3.


#########################################################################
# Prerequisite testing

prereqlist += prereq_getorf_installed

prereq_getorf_installed:
	@$(call checkPrereqPath,getorf,gerorf is part of EMBOSS)

moa_must_define += getorf_input_dir
blast_input_dir_help = directory containing the input sequences

moa_may_define +=  getorf_gff_source
blast_gff_source_help = source field to use in the gff. Defaults to "moa"

moa_may_define += getorf_input_extension
input_extension_help = input file extension. Defaults to 'fasta'

moa_may_define += getorf_minsize getorf_maxsize getorf_circular 		\
	getorf_table getorf_find

getorf_minsize_help = minimal nucleotide size of the predicted ORF,	\
  (**30**)

getorf_maxsize_help = maximal nucleotide size of the predicted ORF,	\
  (**1000000**)

getorf_circular_help = Is the sequence linear (Y/**N**)

getorf_find_help = What to output? 0: Translation between stop codons,	\
  1: Translation between start & stop codon, 2: Nucleotide sequence		\
  between stop codons; 3: Nucleotide sequence between start	\
  and stop codons. Default: 3

getorf_table_help = Genetic code to use: 0 Standard; 1 Standard	\
   with alternative initiation codons; 2 Vertebrate Mitochondrial; 3	\
   Yeast Mitochondrial; 4 Mold, Protozoan, Coelenterate Mitochondrial	\
   and Mycoplasma/Spiroplasma; 5 Invertebrate Mitochondrial; 6 Ciliate	\
   Macronuclear and Dasycladacean; 9 Echinoderm Mitochondrial; 10		\
   Euplotid Nuclear; 11 Bacterial; 12 Alternative Yeast Nuclear; 13		\
   Ascidian Mitochondrial; 14 Flatworm Mitochondrial; 15 Blepharisma	\
   Macronuclear; 16 Chlorophycean Mitochondrial; 21 Trematode			\
   Mitochondrial; 22 Scenedesmus obliquus; 23 Thraustochytrium			\
   Mitochondrial. Default: 11

#preparing for possible gbrowse upload:
gup_gff_dir = ./gff
gup_upload_gff = T
gup_gffsource ?= $(blast_gff_source)

#include moabase, if it isn't already done yet..
include $(shell echo $$MOABASE)/template/moaBase.mk

getorf_table ?= 11
getorf_find ?= 3
getorf_minsize ?= 30
getorf_maxsize ?= 1000000
getorf_circular ?= Y
getorf_gff_source ?= moa
getorf_input_extension ?= fasta
getorf_find ?= 0
getorf_input_files ?= $(wildcard $(getorf_input_dir)/*.$(getorf_input_extension))

getorf_output_files = $(addprefix out/, $(notdir $(patsubst		\
    %.$(getorf_input_extension), %.getorf.fasta, $(getorf_input_files))))

getorf_gff_files = $(addprefix gff/, \
	$(patsubst %.fasta, %.gff, $(notdir $(getorf_output_files))))

getorf_test:
	@echo "Input extension: '$(getorf_input_extension)'"
	@echo "a blastdb file: '$(single_getorf_db_file)'"
	@echo "No inp files $(words $(getorf_input_files))  $(word 1,$(getorf_input_files))"
	@echo "No orf files $(words $(getorf_output_files))  $(word 1,$(getorf_output_files))"
	@echo "No gff files $(words $(getorf_gff_files))  $(word 1,$(getorf_gff_files))"

#echo Main target for getorf
.PHONY: getorf
getorf: $(getorf_gff_files)
	@echo "Done getorfing!"

#prepare for getorf - i.e. create directories
.PHONY: getorf_prepare
getorf_prepare:	
	-mkdir out 
	-mkdir gff  	
	-mkdir fasta

.PHONY: getorf_post
getorf_post:

# Convert to GFF (forward)
gff/%.getorf.gff: out/%.getorf.fasta
	@echo "Create gff $@ from $< - forward genes"
	cat $< 																		\
		| grep "^>" 															\
		| grep -v "REVERSE SENSE"		 										\
		| sed 's/>\(.*\).getorf.\([0-9]*\) \[\([0-9]*\) - \([0-9]*\)\].*/\1\t$(getorf_gff_source)\tCDS\t\3\t\4\t.\t+\t.\tID=\1.getorf.\2;Name=\1.getorf.\2/'	\
		> $@
	@echo "Create gff $@ from $< - reverse genes"
	cat $< 																		\
		| grep "^>" 															\
		| grep "REVERSE SENSE"		 											\
		| sed 's/>\(.*\).getorf.\([0-9]*\) \[\([0-9]*\) - \([0-9]*\)\].*/\1\t$(getorf_gff_source)\tCDS\t\4\t\3\t.\t-\t.\tID=\1.getorf.\2;Name=\1.getorf.\2/'	\
		>> $@

# create out/*xml - run GETORF 
out/%.getorf.fasta: $(getorf_input_dir)/%.$(getorf_input_extension)
	@echo "Processing getorf $*"
	@echo "Creating out.orf $@ from $<"
	@echo "Params $(getorf_program) $(getorf_db)"
	cat $< | getorf -filter -table $(getorf_table) 						\
		-minsize $(getorf_minsize) -maxsize $(getorf_maxsize) 			\
		-circular $(getorf_circular) -find $(getorf_find) 				\
			| sed "s/>$*_\([0-9]*\)/>$*.getorf.\1/" 						\
			>  $@
	fastaSplitter -f $@ -o fasta

getorf_clean:
	-rm -rf ./gff/
	-rm -rf ./out/
	-rm -rf ./fasta/
