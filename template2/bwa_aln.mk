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

#test_2:
#echo 'x' $(if $(bwa_aln_color_space), -c)
#echo 'x' $(if $(call seq,2,2),Equal,Not so)

moa_id = bwa_aln
include $(MOABASE)/lib/gnumake/prepare.mk
include $(MOABASE)/lib/gnumake/core.mk

#Main target
.PHONY: bwa_aln
bwa_aln: $(bwa_aln_output_files)

$(bwa_aln_output_files): %.sai: $(bwa_aln_input_dir)/%.$(bwa_aln_input_extension)
	bwa aln $(bwa_aln_db) 				 					\
			-n $(bwa_aln_edit_dist_missing_prob)     		\
			-o $(bwa_aln_gap_opens_max)              		\
			-e $(bwa_aln_gap_ext_max)      		 			\
			-i $(bwa_aln_no_indel_from_ends)         		\
			-d $(bwa_aln_max_ext_long_del) 		     		\
			-l $(bwa_aln_seed_len) 		             		\
			-k $(bwa_aln_seed_max_diff)              		\
			-m $(bwa_aln_max_queue_entry) 		     		\
			-t $(bwa_aln_thread_num)                 		\
			-M $(bwa_aln_mismatch_penalty) 		     		\
			-O $(bwa_aln_gap_open_penalty)           		\
			-E $(bwa_aln_gap_ext_penalty) 		     		\
			-R $(bwa_aln_best_hits_stop)             		\
			-q $(bwa_aln_quality_step) 						\
			$(if $(bwa_aln_color_space), -c) 				\
			$(if $(bwa_aln_log_gap_penalty_del), -L) 		\
			$(if $(bwa_aln_non_iterative), -N) 				\
			$< -f $@

.PHONY: bwa_aln_clean
bwa_aln_clean:
	-rm -f *.sai

