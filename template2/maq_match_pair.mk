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

moa_id = maq_match_pair

#variables

ifndef dont_include_moabase
	include $(shell echo $$MOABASE)/template/moa/core.mk
endif

##### Derived variables for this run

forward_files = $(wildcard $(maq_match_pair_read_dir)/*$(maq_match_pair_forward_suffix))
maq_match_pair_outfiles = $(addsuffix .out,\
		$(patsubst %$(maq_match_pair_forward_suffix),%,$(notdir $(forward_files))))

test:
	@echo $(forward_files)
	$e echo
	@echo $(maq_match_pair_outfiles)

.PHONY: maq_match_pair_prepare
maq_match_pair_prepare:

.PHONY: maq_match_pair_post
maq_match_pair_post:

maq_match_pair: $(maq_match_pair_outfiles)

$(maq_match_pair_outfiles): %.out : \
	$(maq_match_pair_reference) \
	$(maq_match_pair_read_dir)/%$(maq_match_pair_forward_suffix) \
	$(maq_match_pair_read_dir)/%$(maq_match_pair_reverse_suffix)
	$e maq map -A $(maq_match_pair_RF_maxdist) -a $(maq_match_pair_maxdist) $@ $?

bfq/%.bfq: $(maq_match_pair_input_dir)/%.$(maq_match_pair_input_extension)
	maq fastq2bfq $< $@

maq_match_pair_clean:
	$e -rm -rf *.out

