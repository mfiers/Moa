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

moa_id += bdbb

bdbb_help = generate a list of bidirectional best blast hits.


#########################################################################
# Prerequisite testing

moa_prereq_simple += blastall formatdb

moa_must_define += bdbb_input_fila_a
bdbb_input_fila_a_help = First multifasta input file
bdbb_input_fila_a_type = file

moa_must_define += bdbb_input_fila_b
bdbb_input_fila_b_help = First multifasta input file
bdbb_input_fila_b_type = file

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

bdbb_test:
	$(e)echo "Input extension: '$(bdbb_input_extension)'"
	$(e)echo "Real blast db  '$(real_bdbb_db)'"
	$(e)echo "a blastdb file: '$(single_bdbb_db_file)'"
	$(e)echo "real blast db: '$(real_bdbb_db)'"
	$(e)echo "No inp files $(words $(bdbb_input_files))"
	$(e)echo "No xml files $(words $(bdbb_output_files))"
	$(e)echo "No gff files $(words $(bdbb_gff_files))"

#echo Main target for blast
.PHONY: blast
bdbb: bdbb_output

bdbb_output: bdbb_first_phase

bdbb_first_phase: bdbb_blast_db_a
	formatdb
	blastall -i $(bdbb_input_fila_a)

bdbb_blast_db_a:
	formatdb -i $(bdbb_input_fila_a) \-
		-p $(bdbb_protein)


#prepare for blast - i.e. create directories
.PHONY: bdbb_prepare
bdbb_prepare:

.PHONY: bdbb_post
bdbb_post:

# create out/*xml - run BLAST 
output:
	$(e) $(call echo,Running BLAST on $<)
	$(e)echo "Processing blast $*"
	$(e)echo "Creating out.xml $@ from $<"
	$(e)echo "Params $(bdbb_program) $(bdbb_db)"
	blastall -i $< -p $(bdbb_program) -e $(bdbb_eval) -m 7 \
		-a $(bdbb_nothreads) -d $(real_bdbb_db) \
		-b $(bdbb_nohits) -v $(bdbb_nohits) \
		-o $@


bdbb_clean:
	-rm -rf output