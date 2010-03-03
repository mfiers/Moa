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

################################################################################
#include moabasepre
include $(MOABASE)/template/moa/prepare.mk

moa_title = Getorf

moa_description = Predicts open reading frames using the EMBOSS	\
  [[emboss]] getorf tool.

moa_prerequisites += The [EMBOSS]() [[emboss]] suite of tools

moa_id += getorf

moa_getorf_help = Getorf is a open reading frame discovery program		\
  from the EMBOSS [[emboss]] package. It takes a set of input			\
  sequences and predicts all open reading frames. Additionally, this	\
  template converts the default output (predicted protein sequences)	\
  to GFF3.


#########################################################################
# Prerequisite testing
moa_prereq_simple += getorf

#########################################################################
# Variable definition

$(call moa_fileset_define,getorf_input,fasta,Input files for getorf)

moa_may_define +=  getorf_gff_source
getorf_gff_source_help = source field to use in the gff.
getorf_gff_source_type = string
getorf_gff_source_default = getorf

moa_may_define += getorf_minsize getorf_maxsize getorf_circular 		\
	getorf_table getorf_find

getorf_minsize_help = minimal nucleotide size of the predicted ORF.
getorf_minsize_type = integer
getorf_minsize_default = 30

getorf_maxsize_help = maximal nucleotide size of the predicted ORF.
getorf_maxsize_type = integer
getorf_maxsize_default = 1000000

getorf_circular_help = Is the sequence linear?
getorf_circular_type = set
getorf_circular_allowed = Y N
getorf_circular_default = N

getorf_find_help = What to output? 0: Translation between stop codons,	\
  1: Translation between start & stop codon, 2: Nucleotide sequence		\
  between stop codons; 3: Nucleotide sequence between start	\
  and stop codons. Default: 3
getorf_find_type = set
getorf_find_allowed = 0 1 2 3 
getorf_find_default = 3

getorf_table_help = Genetic code to use: 0 Standard; 1 Standard	\
   with alternative initiation codons; 2 Vertebrate Mitochondrial; 3	\
   Yeast Mitochondrial; 4 Mold, Protozoan, Coelenterate Mitochondrial	\
   and Mycoplasma/Spiroplasma; 5 Invertebrate Mitochondrial; 6 Ciliate	\
   Macronuclear and Dasycladacean; 9 Echinoderm Mitochondrial; 10		\
   Euplotid Nuclear; 11 Bacterial; 12 Alternative Yeast Nuclear; 13		\
   Ascidian Mitochondrial; 14 Flatworm Mitochondrial; 15 Blepharisma	\
   Macronuclear; 16 Chlorophycean Mitochondrial; 21 Trematode			\
   Mitochondrial; 22 Scenedesmus obliquus; 23 Thraustochytrium			\
   Mitochondrial.
getorf_table_type = set
getorf_table_allowed = 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 21 22 23
getorf_table_default = 11

################################################################################
#include moabase
include $(MOABASE)/template/moa/core.mk

getorf_gff_source ?= moa
getorf_input_extension ?= fasta
getorf_find ?= 0

#prepare lists of out & gff files
$(call moa_fileset_remap,getorf_input,getorf_output,out)
$(call moa_fileset_remap,getorf_input,getorf_gff,gff)

	
#echo Main target for getorf
.PHONY: getorf
getorf: $(getorf_gff_files)
	@echo "Done getorfing!"

#prepare for getorf - i.e. create directories
.PHONY: getorf_prepare
getorf_prepare:	
	-mkdir out 
	-mkdir gff  	

.PHONY: getorf_post
getorf_post:

# Convert to GFF (forward)
gff/%.gff: out/%.out
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

# create getorf/*xml - run GETORF 
out/%.out: $(getorf_input_dir)/%.$(getorf_input_extension)
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
	
getorf_test:
	$e echo "testing getorf (datadir $(MOADATA))"
	moa new -f -t 'testing getorf' getorf
	moa set getorf_input_dir=$(MOADATA)/10.dna
	[[ -f gff/test.gff ]] || $(call exer,No output file is generated)
	[[ "`cat gff/test.gff | wc -l`"  == "354" ]] || $(call errr,Unexpected number of discovered ORFs)
	
