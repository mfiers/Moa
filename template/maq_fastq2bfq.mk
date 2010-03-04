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

moa_id = fq2bq
moa_title_maq_fasta2bfa = Convert FASTQ to BFQ
moa_description_maq_fasta2bfa = Converts a FASTQ file to MAQ BFQ	\
format.

#variables
$(call moa_fileset_define,fq2bq_input,fastq,input FASTA files)

ifndef dont_include_moabase
	include $(shell echo $$MOABASE)/template/moa/core.mk
endif

##### Derived variables for this run

#$(call moa_fileset_init,fq2bq_input)
$(call moa_fileset_remap,fq2bq_input,fq2bq_bfq,bfq)

test:
	@echo $(fq2bq_input_files)
	$e echo
	$e echo
	@echo $(fq2bq_bfq_files)

.PHONY: fq2bq_prepare
fq2bq_prepare:
	-mkdir bfq

.PHONY: fq2bq_post
fq2bq_post:

fq2bq: $(fq2bq_bfq_files)

bfq/%.bfq: $(fq2bq_input_dir)/%.$(fq2bq_input_extension)
	maq fastq2bfq $< $@

fq2bq_clean:
	$e -rm -rf bfa





