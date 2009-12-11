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

ifndef dont_include_moabase
	include $(shell echo $$MOABASE)/template/moaBasePre.mk
endif

moa_ids += f2b
moa_title_maq_fasta2bfa = Convert fasta to bfa
moa_description_maq_fasta2bfa = Converts a FASTA file to MAQ format	\
for use with a BFA a maq_fasta2bfa index from a reference sequence

#variables
$(call moa_fileset_define,f2b_input,fasta,input FASTA files)

ifndef dont_include_moabase
	include $(shell echo $$MOABASE)/template/moaBase.mk
endif

##### Derived variables for this run

$(call moa_fileset_init,f2b_input)
$(call moa_fileset_remap,f2b_input,f2b_bfa,bfa)

test:
	@echo $(f2b_input_files)
	$e echo
	$e echo
	@echo $(f2b_bfa_files)

.PHONY: f2b_prepare
f2b_prepare:
	-mkdir bfa

.PHONY: f2b_post
f2b_post:

f2b: $(f2b_bfa_files)

bfa/%.bfa: $(f2b_input_dir)/%.$(f2b_input_extension)
	maq fasta2bfa $< $@

comma:=,
#one of the database files
$(f2b_name).1.ebwt: $(maq_fasta2bfa_input_files)
	$e -rm -f $(maq_fasta2bfa_name).*.ebwt	
	$e maq_fasta2bfa-build $(call merge,$(comma),$^) $(maq_fasta2bfa_name)

f2b_clean:
	$e -rm -rf bfa





