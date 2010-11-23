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
moa_id = blastdb
template_title_blastdb = Create a BLAST database

#Variable: protein

#Include base moa code - does variable checks & generates help
include $(MOABASE)/lib/gnumake/core.mk
# End of the generic part - from here on you're on your own :)

bdb_doconcat = F
ifndef bdb_fasta_file
  bdb_doconcat = T
  bdb_fasta_file = $(bdb_name).fasta
  input_files ?= $(wildcard $(bdb_input_dir)/*.$(bdb_input_extension))
else
  bdb_doconcat = F
endif

#the rest of the variable definitions

ifeq ("$(bdb_protein)", "F")
	one_blast_db_file = $(bdb_name).nhr
else
	one_blast_db_file = $(bdb_name).phr
endif

blastdb_prepare:

blastdb_post: create_id_list

blastdb: $(one_blast_db_file)

$(one_blast_db_file): $(bdb_fasta_file)
	@echo "Creating $@ from $(bdb_input_dir)"
	formatdb -i $< -p $(bdb_protein) -o T -n $(bdb_name)
	touch $(bdb_name)

$(bdb_fasta_file): $(input_files)
	if [[ "$(bdb_doconcat)" == "T" ]]; then 		\
		$(call echo,Starting concat $(bdb_coconcat) -)	\
		find $(bdb_input_dir) -type f 			\
	 		-name "*.$(bdb_input_extension)" 	\
			| xargs -n 100 cat 			\
			> $(bdb_fasta_file); 			\
		fi

.PHONY: create_id_list
create_id_list: $(bdb_name).list

$(bdb_name).list: $(bdb_fasta_file)
	grep ">" $(bdb_fasta_file) | cut -c2- | sed 's/ /\t/' | sort > $(bdb_name).list

blastdb_clean:	
	-if [ $(bdb_protein) == "F" ]; then \
		rm $(bdb_name).n?? ;\
	else \
		rm $(bdb_name).p?? ;\
	fi
	-rm $(bdb_name).list
	-rm formatdb.log

