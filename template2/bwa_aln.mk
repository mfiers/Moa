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

include $(MOABASE)/lib/gnumake/prepare.mk
moa_id = bwa_aln

#########################################################################
# Prerequisite testing

#variables

$(moa_id)_seed_len_formatter = -l $(1)

include $(MOABASE)/lib/gnumake/core.mk

$(bwa_aln_output_files): %.sai: $(bwa_aln_input_dir)/%.$(bwa_aln_input_extension)
	bwa aln $($(moa_id)_db) $($(moa_id)_seed_len_f) $< -f $@

bwa_aln: $(bwa_aln_output_files)

bwa_aln_clean:
	-rm -f *.sai

