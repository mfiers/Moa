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

moa_id = revseq

#########################################################################
# Prerequisite testing

#########################################################################
# Variable definition

################################################################################
#include moabase
include $(MOABASE)/lib/gnumake/core.mk
revseq_gff_source ?= moa
revseq_input_extension ?= fasta
revseq_find ?= 0

#prepare lists of out & gff files

#echo Main target for revseq
.PHONY: revseq
revseq: $(revseq_gff_files)
	@echo "Done revseqing!"

#prepare for revseq - i.e. create directories
.PHONY: revseq_prepare
revseq_prepare:	
	-mkdir out 
	-mkdir gff

.PHONY: revseq_post
revseq_post:

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

