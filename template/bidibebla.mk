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

moa_title = Bidirectional best BLAST hit
moa_description = Discover the bidirectional best blast hit between two \
  sets of sequences
moa_prerequisites += The [BLAST](http://www.ncib.nlm.nih.gov/blast)		\
  [[Alt90]] suite of tools

moa_id = bdbb

bdbb_help = generate a list of bidirectional best blast hits.


#########################################################################
# Prerequisite testing

moa_prereq_simple += blastall formatdb

moa_must_define += bdbb_input_file_a
bdbb_input_file_a_help = First multifasta input file
bdbb_input_file_a_type = file

moa_must_define += bdbb_input_file_b
bdbb_input_file_b_help = First multifasta input file
bdbb_input_file_b_type = file

moa_may_define += bdbb_protein
bdbb_protein_type = set
bdbb_protein_help = Are we looking at proteins?
bdbb_protein_default = F
bdbb_protein_allowed= T F

moa_may_define += bdbb_eval
bdbb_eval_default = 1e-10
bdbb_eval_help = e value cutoff
bdbb_eval_type = float

moa_may_define += bdbb_nothreads
bdbb_nothreads_default = 4
bdbb_nothreads_help = threads to run bdbb with (note the overlap \
	with the Make -j parameter)
bdbb_nothreads_type = integer

#include moabasemoa	
include $(MOABASE)/template/moa/core.mk

#echo Main target for blast
.PHONY: blast
bdbb: bdbb_output

bdbb_output: blast_program=$(if $(call seq,$(bdbb_protein),T),blastp,blastn)
bdbb_output: baseA=$(shell basename $(bdbb_input_file_a))
bdbb_output: baseB=$(shell basename $(bdbb_input_file_b))
bdbb_output:
	formatdb -i $(bdbb_input_file_a) -n $(baseA) \
		-p $(bdbb_protein)
	formatdb -i $(bdbb_input_file_b) -n $(baseB) \
		-p $(bdbb_protein)
	blastall -p $(blast_program) -i $(bdbb_input_file_a) \
		-d $(baseB) -m 8 -v 1 -b 1 \
		-e $(bdbb_eval) \
		> $(baseA).out 
	blastall -p $(blast_program) -i $(bdbb_input_file_b) \
		-d $(baseA) -m 8 -b 1 -v 1 \
		-e $(bdbb_eval) \
		> $(baseB).out 
	cat  $(baseA).out | cut -f-2 | awk '{print $$1 "___" $$2}' | sort | uniq > listA
	cat  $(baseB).out | cut -f-2 | awk '{print $$2 "___" $$1}' | sort | uniq > listB
	-rm -f bidibebla
	for x in `cat listB`; do \
		if grep -q $$x listA; then \
			echo $$x | sed "s/___/\t/" >> bidibebla ;\
		fi; \
	done
	echo -n "sequences in $(bdbb_input_file_a): " > report
	grep ">" $(bdbb_input_file_a) | wc -l >> report
	echo -n "sequences in $(bdbb_input_file_b): " >> report
	grep ">" $(bdbb_input_file_b) | wc -l >> report
	echo -n "number of best biderectional pairs found: " >> report
	cat bidibebla | wc -l  >> report

bdbb_clean:
	-rm -rf *nin *nsq *out *nhr listA listB bidibebla