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
	include $(shell echo $$MOABASE)/template/moa/prepare.mk
endif

moa_id = maq_fasta2bfa

#variables

ifndef dont_include_moabase
	include $(shell echo $$MOABASE)/template/moa/core.mk
endif

##### Derived variables for this run

test:
	@echo $(maq_fasta2bfa_input_files)
	$e echo
	$e echo
	@echo $(maq_fasta2bfa_bfa_files)

.PHONY: maq_fasta2bfa_prepare
maq_fasta2bfa_prepare:
	-mkdir bfa

.PHONY: maq_fasta2bfa_post
maq_fasta2bfa_post:

maq_fasta2bfa: $(maq_fasta2bfa_bfa_files)

bfa/%.bfa: $(maq_fasta2bfa_input_dir)/%.$(maq_fasta2bfa_input_extension)
	maq fasta2bfa $< $@

comma:=,
#one of the database files
$(maq_fasta2bfa_name).1.ebwt: $(maq_fasta2bfa_input_files)
	$e -rm -f $(maq_fasta2bfa_name).*.ebwt	
	$e maq_fasta2bfa-build $(call merge,$(comma),$^) $(maq_fasta2bfa_name)

maq_fasta2bfa_clean:
	$e -rm -rf bfa

