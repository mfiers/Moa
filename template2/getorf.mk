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
include $(MOABASE)/lib/gnumake/prepare.mk

moa_id = getorf

#########################################################################
# Prerequisite testing

#########################################################################
# Variable definition

################################################################################
#include moabase
include $(MOABASE)/lib/gnumake/core.mk
getorf_gff_source ?= moa
getorf_input_extension ?= fasta
getorf_find ?= 0

#prepare lists of out & gff files

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

