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

include $(MOABASE)/template/moa/prepare.mk

moa_id = bowtiedb
template_title = Bowtie index builder
template_description = Builds a bowtie index from a reference sequence


#########################################################################
# Prerequisite testing
moa_prereq_simple += bowtie-build

#variables
$(call moa_fileset_define,bowtiedb_input,fasta,Sequence files used to build a bowtie database)

moa_must_define += bowtiedb_name
bowtiedb_name_help = Name of the bowtie index to create
bowtiedb_name_type = string

include $(MOABASE)/template/moa/core.mk

bowtiedb: $(bowtiedb_name).1.ebwt

#one of the database files
$(bowtiedb_name).1.ebwt: $(bowtiedb_input_files)
	-$e rm -f $(bowtiedb_name).*.ebwt
	$e bowtie-build $(call merge,$(comma),$^) $(bowtiedb_name)
	touch $(bowtiedb_name)

bowtiedb_clean:
	-rm -f $(bowtiedb_name).*.ebwt

