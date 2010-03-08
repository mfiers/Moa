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

moa_id = crunch

crunch_help = generate a list of bidirectional best blast hits.


#########################################################################
# Prerequisite testing

moa_prereq_simple += blastall formatdb

moa_must_define += crunch_input_fila_a
crunch_input_fila_a_help = First multifasta input file
crunch_input_fila_a_type = file

moa_must_define += crunch_input_fila_b
crunch_input_fila_b_help = First multifasta input file
crunch_input_fila_b_type = file

moa_may_define += crunch_protein
crunch_protein_type = set
crunch_protein_help = Are we looking at proteins?
crunch_protein_default = F
crunch_protein_allowed= T F

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

crunch_test:
	$(e)echo "Input extension: '$(crunch_input_extension)'"
	$(e)echo "Real blast db  '$(real_crunch_db)'"
	$(e)echo "a blastdb file: '$(single_crunch_db_file)'"
	$(e)echo "real blast db: '$(real_crunch_db)'"
	$(e)echo "No inp files $(words $(crunch_input_files))"
	$(e)echo "No xml files $(words $(crunch_output_files))"
	$(e)echo "No gff files $(words $(crunch_gff_files))"

#echo Main target for blast
.PHONY: blast
crunch: crunch_output

crunch_output: crunch_first_phase

crunch_first_phase: crunch_blast_db_a
	formatdb
	blastall -i $(crunch_input_fila_a)

crunch_blast_db_a:
	formatdb -i $(crunch_input_fila_a) \-
		-p $(crunch_protein)


#prepare for blast - i.e. create directories
.PHONY: crunch_prepare
crunch_prepare:

.PHONY: crunch_post
crunch_post:

# create out/*xml - run BLAST 
output:
	$(e) $(call echo,Running BLAST on $<)
	$(e)echo "Processing blast $*"
	$(e)echo "Creating out.xml $@ from $<"
	$(e)echo "Params $(crunch_program) $(crunch_db)"
	blastall -i $< -p $(crunch_program) -e $(crunch_eval) -m 7 \
		-a $(crunch_nothreads) -d $(real_crunch_db) \
		-b $(crunch_nohits) -v $(crunch_nohits) \
		-o $@


crunch_clean:
	-rm -rf output