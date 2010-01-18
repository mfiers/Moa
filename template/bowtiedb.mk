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
moa_ids += bowtiedb
moa_title_bowtiedb = Bowtie index builder
moa_description_bowtiedb = Builds a bowtie index from a reference sequence

#variables
moa_must_define += bowtiedb_input_dir
bowtiedb_input_dir_help = The reference sequence to build a bowtie database with.
bowtiedb_input_dir_type = directory

moa_may_define += bowtiedb_input_extension
bowtiedb_input_extension_default = .1.ebwt
bowtiedb_input_extension_help = Extension of the input files, defaults to 'fasta'
bowtiedb_input_extension_type = string

moa_must_define += bowtiedb_name
bowtiedb_name_help = Name of the bowtie index to create
bowtiedb_name_type = string

ifndef dont_include_moabase
	include $(shell echo $$MOABASE)/template/moaBase.mk
endif

##### Derived variables for this run
moa_register_extra += bowtiedb
moa_register_bowtiedb = $(shell echo `pwd`)/$(bowtiedb_name)

bowtiedb_input_files = $(wildcard $(bowtiedb_input_dir)/*.$(bowtiedb_input_extension))

test:
	@echo $(bowtiedb_input_files)

.PHONY: bowtiedb_prepare
bowtiedb_prepare:

.PHONY: bowtiedb_post
bowtiedb_post:

bowtiedb: $(bowtiedb_name).1.ebwt

comma:=,
#one of the database files
$(bowtiedb_name).1.ebwt: $(bowtiedb_input_files)
	-rm -f $(bowtiedb_name).*.ebwt	
	bowtie-build $(call merge,$(comma),$^) $(bowtiedb_name)

bowtiedb_clean:
	-rm -f $(bowtiedb_name).*.ebwt

