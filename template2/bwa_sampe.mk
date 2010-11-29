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
moa_id = bwa_sampe
include $(MOABASE)/lib/gnumake/prepare.mk
include $(MOABASE)/lib/gnumake/core.mk

#main target, called when moa run is executed
$(moa_id): $($(moa_id)_output_files)

#process each of the output files, based on the input files
#-n $(bwa_samse_max_aln_out) \

$($(moa_id)_output_files): sai1_file=$($(moa_id)_input_sai1_dir)/$*.sai
$($(moa_id)_output_files): sai1_file=$($(moa_id)_input_sai2_dir)/$*.sai

$($(moa_id)_output_files): 							\
			%.$($(moa_id)_output_extension): 			\
			$($(moa_id)_input_dir)/%.$($(moa_id)_input_extension)
	#echo $(sai_file) $< -f $@
	echo bwa sampe -a $($(moa_id)_max_insert_size)     		\
			  -o $($(moa_id)_max_occ_read)     		    \
			  -n $($(moa_id)_max_aln_out)     		    \
			  -N $($(moa_id)_max_out_discordant_pairs)  \
			  -c $($(moa_id)_prior_chimeric_rate)     	\
			  $(if $($(moa_id)_preload_index), -P) 		\
			  $(if $($(moa_id)_disable_SW), -s) 		\
			  $(if $($(moa_id)_disable_insert_size), -A)\
			  $(sai1_file) $(sai2_file) \
			  $< -f $@

$(moa_id)_clean:
	-rm -f *.$($(moa_id)_output_extension)
