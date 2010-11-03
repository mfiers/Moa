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
moa_id = repmask

$(call moa_fileset_define,$(moa_id)_input,fasta,Input files for $(moa_id))

#variables

repmask_species_formatter = $(if $(1),-spe $(1))

$(moa_id)_simple_formatter = $(if $(call seq,$(1),T),-int,noint)

$(moa_id)_quick_formatter = $(if $(call seq,$(1),T),-qq)

$(moa_id)_parallel_formatter = -pa $(1)

include $(MOABASE)/lib/gnumake/core.mk## usage: $(call moa_fileset_remap,INPUT_FILESET_ID,OUTPUT_FILESET_ID,OUTPUT_FILETYPE)
$(call moa_fileset_remap_nodir,$(moa_id)_input,$(moa_id)_output,masked)

.PHONY: repmask_prepare
repmask_prepare:

.PHONY: repmask_post
repmask_post:

.PHONY: repmask
repmask: $($(moa_id)_output_files)

./%.masked: $($(moa_id)_input_dir)/%.$($(moa_id)_input_extension)
	ln $< . -s
	$e RepeatMasker \
		$($(moa_id)_simple_f) \
		$($(moa_id)_quick_f) \
		$($(moa_id)_species_f) \
		$($(moa_id)_parallel_f) \
		`basename $<`

repmask_clean:

