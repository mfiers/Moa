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

moa_id = bwa_aln
template_title = BWA align
template_description = Use bwa to aling a set of fastq reads against a	\
  db

#########################################################################
# Prerequisite testing
moa_prereq_simple += bwa

#variables
$(call moa_fileset_define,bwa_aln_input,fq,Fastq input files)

moa_must_define += $(moa_id)_db
$(moa_id)_db_help = bwa database to align against
$(moa_id)_db_type = file

moa_may_define += $(moa_id)_seed_len
$(moa_id)_seed_len_help = Seed length
$(moa_id)_seed_len_type = integer
$(moa_id)_seed_len_default =
$(moa_id)_seed_len_formatter = -l $(1)


include $(MOABASE)/template/moa/core.mk

$(call moa_fileset_remap_nodir,bwa_aln_input,bwa_aln_output,sai)

$(bwa_aln_output_files): %.sai: $(bwa_aln_input_dir)/%.$(bwa_aln_input_extension)
	bwa aln $($(moa_id)_db) $($(moa_id)_seed_len_f) $< -f $@

bwa_aln: $(bwa_aln_output_files)

bwa_aln_clean:
	-rm -f *.sai

