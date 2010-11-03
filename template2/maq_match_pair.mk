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

moa_id = maqpair

#variables

ifndef dont_include_moabase
	include $(shell echo $$MOABASE)/template/moa/core.mk
endif

##### Derived variables for this run

forward_files = $(wildcard $(maqpair_read_dir)/*$(maqpair_forward_suffix))
maqpair_outfiles = $(addsuffix .out,\
		$(patsubst %$(maqpair_forward_suffix),%,$(notdir $(forward_files))))

test:
	@echo $(forward_files)
	$e echo
	@echo $(maqpair_outfiles)

.PHONY: maqpair_prepare
maqpair_prepare:

.PHONY: maqpair_post
maqpair_post:

maqpair: $(maqpair_outfiles)

$(maqpair_outfiles): %.out : \
	$(maqpair_reference) \
	$(maqpair_read_dir)/%$(maqpair_forward_suffix) \
	$(maqpair_read_dir)/%$(maqpair_reverse_suffix)
	$e maq map -A $(maqpair_RF_maxdist) -a $(maqpair_maxdist) $@ $?

bfq/%.bfq: $(maqpair_input_dir)/%.$(maqpair_input_extension)
	maq fastq2bfq $< $@

maqpair_clean:
	$e -rm -rf *.out

