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
moa_id = vmatchdb

#variables

$(call moa_fileset_define,vmatchdb_input,fasta,Input files for vmatch)

ifndef dont_include_moabase
	include $(shell echo $$MOABASE)/template/moa/core.mk
endif

##### Derived variables for this run
moa_register_extra += vmatchdb
moa_register_vmatchdb = $(shell echo `pwd`)/$(vmatchdb_name)

vmatchdb_input_extension ?= fasta

vmatchdb_input_files = $(wildcard $(vmatchdb_input_dir)/*.$(vmatchdb_input_extension))

.PHONY: vmatchdb_prepare
vmatchdb_prepare:
	@echo "--" $(vmatchdb_input_files)

.PHONY: vmatchdb_post
vmatchdb_post:

.PHONY: vmatchdb
vmatchdb: $(vmatchdb_input_files)
	@echo processing $(words $^) input files
	-rm -f $(vmatchdb_name).fasta
	if [[ $(words $^) > 1 ]]; then								\
		cat $^ > $(vmatchdb_name).fasta;						\
	else														\
		ln -s $(vmatchdb_input_dir)/$< $(vmatchdb_name).fasta;	\
	fi;
	mkvtree -db $(vmatchdb_name).fasta -dna -allout	\
		-v -pl $(vmatchdb_pl)						\
		-indexname $(vmatchdb_name).fasta

.PHONY: vmatchdb_clean
vmatchdb_clean:
	rm $(vmatchdb_name).fasta*