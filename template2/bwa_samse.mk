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
moa_id = bwa_samse
include $(MOABASE)/lib/gnumake/prepare.mk
include $(MOABASE)/lib/gnumake/core.mk

#main target, called when moa run is executed
$(moa_id): $($(moa_id)_output_files)

$($(moa_id)_output_files): sai_file=$($(moa_id)_input_sai_dir)/$*.sai
$($(moa_id)_output_files): %.$($(moa_id)_output_extension): \
			$($(moa_id)_input_dir)/%.$($(moa_id)_input_extension)
	bwa samse -n $(bwa_samse_max_aln_out) \
				$($(moa_id)_db) \
				$(sai_file) $< > $@
#		| samtools view -bhS - > $@
#	samtools index $@

$(moa_id)_clean:
	-rm -f *.$($(moa_id)_output_extension)

