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

moa_id = bwa_aln
include $(MOABASE)/lib/gnumake/prepare.mk
include $(MOABASE)/lib/gnumake/core.mk

test_2:
	echo $(bwa_aln_output_files)
	echo $(bwa_aln_input_files)

#Main target
.PHONY: bwa_aln
bwa_aln: $(bwa_aln_output_files)

$(bwa_aln_output_files): %.sai: $(bwa_aln_input_dir)/%.$(bwa_aln_input_extension)
	bwa aln $(bwa_aln_db) 				\
			-l $(bwa_aln_seed_len) 		\
			-k $(bwa_aln_seed_max_diff) \
			$< -f $@

.PHONY: bwa_aln_clean
bwa_aln_clean:
	-rm -f *.sai

