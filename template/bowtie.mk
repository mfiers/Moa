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
moa_ids += bowtie 
moa_title_bowtie = Bowtie
moa_description_bowtie = Run BOWTIE on an set of input files (query) \
  vs a database index.

#variables
moa_must_define += bowtie_db
bowtie_db_help = Bowtie db
bowtie_db_default_attrib = bowtiedb

moa_must_define += bowtie_input_dir
bowtie_input_dir_help = input dir with the query files

moa_may_define += bowtie_input_extension
bowtie_input_extension_help = Extension of the input files, \
  defaults to fastq

moa_may_define += bowtie_input_format
bowtie_input_format_help = Format of the input files, defaults \
  to fastq

moa_may_define += bowtie_extra_params
bowtie_extra_params_help = extra parameters to feed bowtie

moa_may_define += bowtie_output_name
bowtie_output_name_gelp = output file name, defaults to 'output'

ifndef dont_include_moabase
	include $(shell echo $$MOABASE)/template/moaBase.mk
endif

##### Derived variables for this run


bowtie_input_extension ?= fastq
bowtie_input_format ?= fastq
bowtie_output_name ?= output

moa_register_extra += bowtie_output
moa_register_bowtie_output = $(shell echo `pwd`)/$(bowtie_output_name)

ifeq ($(bowtie_input_format),fastq)
bowtie_input_format_param = -q
endif
ifeq ($(bowtie_input_format),fasta)
bowtie_input_format_param = -f
endif
ifndef bowtie_input_format_param
$(error Invalid input format)
endif

bowtie_input_files = $(wildcard $(bowtie_input_dir)/*.$(bowtie_input_extension))

.PHONY: bowtie_prepare
bowtie_prepare:

.PHONY: bowtie_post
bowtie_post: 

test:
	@echo $(bowtie_input_files)

comma:=,
.PHONY: bowtie
bowtie: $(bowtie_output_name) 

$(bowtie_output_name): $(bowtie_input_files)
	bowtie $(bowtie_input_format_param) \
		-p $(MOA_PROCESSORS) \
		$(bowtie_extra_params) \
		$(bowtie_db) \
		$(call merge,$(comma),$^) \
		output

bowtie_clean:
	-rm -f $(bowtie_output_name)


