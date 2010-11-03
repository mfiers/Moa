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

moa_id = crunch

#########################################################################
# Prerequisite testing

#include moabasemoa	
include $(MOABASE)/lib/gnumake/core.mk
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