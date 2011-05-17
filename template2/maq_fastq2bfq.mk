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

moa_id = maq_fastq2bfq

#variables

ifndef dont_include_moabase
	include $(shell echo $$MOABASE)/template/moa/core.mk
endif

##### Derived variables for this run

#$(call moa_fileset_init,maq_fastq2bfq_input)

test:
	@echo $(maq_fastq2bfq_input_files)
	$e echo
	$e echo
	@echo $(maq_fastq2bfq_bfq_files)

.PHONY: maq_fastq2bfq_prepare
maq_fastq2bfq_prepare:
	-mkdir bfq

.PHONY: maq_fastq2bfq_post
maq_fastq2bfq_post:

maq_fastq2bfq: $(maq_fastq2bfq_bfq_files)

bfq/%.bfq: $(maq_fastq2bfq_input_dir)/%.$(maq_fastq2bfq_input_extension)
	maq fastq2bfq $< $@

maq_fastq2bfq_clean:
	$e -rm -rf bfa

