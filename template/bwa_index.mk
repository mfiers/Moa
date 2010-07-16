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

moa_id = bwa_index
template_title = Bwa index builder
template_description = Builds a bwa index from a reference sequence

#########################################################################
# Prerequisite testing
moa_prereq_simple += bwa-build

#variables
$(call moa_fileset_define,bwa_index_input,fasta,Sequence files used to build a bwa database)

moa_must_define += bwa_index_name
bwa_index_name_help = Name of the bwa index to create
bwa_index_name_type = string

include $(MOABASE)/template/moa/core.mk

fastafile = $(notdir $(bwa_index_name)).fasta


$(fastafile): $(bwa_index_input_files)
	cat $^ > $@

$(bwa_index_name).amb: @.amb : $(fastafile)
	bwa index -p $* -a IS $<
	touch $*

bwa_index: $(bwa_index_name).amb

bwa_index_clean:
	-rm -f $(bwa_index_name).*

