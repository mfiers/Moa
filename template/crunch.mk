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

moa_title = Create ACT crunch files for use with Artemis ACT
moa_description = Create a crunch file for use with the Artemis ACT \
  comparison tool. 

moa_id = crunch

crunch_help = create crunch files


#########################################################################
# Prerequisite testing

moa_prereq_simple += blastall formatdb

$(call moa_fileset_define,crunch_input,fasta,Directory with input fasta files)

moa_may_define += crunch_eval
crunch_eval_default = 1e-10
crunch_eval_help = e value cutoff
crunch_eval_type = float

moa_may_define += crunch_nothreads
crunch_nothreads_default = 4
crunch_nothreads_help = threads to run crunch with (note the overlap \
	with the Make -j parameter)
crunch_nothreads_type = integer

#include moabasemoa	
include $(MOABASE)/template/moa/core.mk

#shortcut - need this quite  often
ext = $(crunch_input_extension)

#echo Main target for blast
.PHONY: blast

crunch_output_files=$(foreach f1, $(crunch_input_files), \
	$(foreach f2, $(crunch_input_files), \
		crunch_$(patsubst %.$(ext),%,$(notdir $(f1)))___$(patsubst %.$(ext),%,$(notdir $(f2)))))

crunch_test:
	echo $(crunch_input_files)
	echo $(crunch_output_files)		
crunch: $(crunch_output_files)


crunch_%:
	f1=`echo "$*" | sed "s/^.*___//"` ;\
		f2=`echo "$*" | sed "s/___.*$$//"`	;\
		$(call echo, Processing $$f1 $$f2) ;\
		formatdb -i $(crunch_input_dir)/$$f2.$(ext) -p F -n $$f2; 	\
		blastall -p blastn -a $(crunch_nothreads) -m 8 		\
			-i $(crunch_input_dir)/$$f1.$(ext) -d $$f2 -o $@;			\
		rm $$f2.n??

crunch_clean:
	-rm -f crunch_*