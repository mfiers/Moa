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
moa_id = blastdb
include $(MOABASE)/lib/gnumake/prepare.mk
include $(MOABASE)/lib/gnumake/core.mk
#the rest of the variable definitions

ifeq ("$(blastdb_protein)", "F")
	one_blast_db_file = $(blastdb_name).nhr
else
	one_blast_db_file = $(blastdb_name).phr
endif

blastdb_prepare:

blastdb_post: create_id_list

blastdb: $(one_blast_db_file)

$(one_blast_db_file): $(blastdb_fasta_file)
	@echo "Creating $@ from $(blastdb_input_dir)"
	formatdb -i $< -p $(blastdb_protein) -o T -n $(blastdb_name)
	touch $(blastdb_name)

$(blastdb_fasta_file): $(input_files)
	if [[ "$(blastdb_doconcat)" == "T" ]]; then 		\
		$(call echo,Starting concat $(blastdb_coconcat) -)	\
		find $(blastdb_input_dir) -type f 			\
	 		-name "*.$(blastdb_input_extension)" 	\
			| xargs -n 100 cat 			\
			> $(blastdb_fasta_file); 			\
		fi

.PHONY: create_id_list
create_id_list: $(blastdb_name).list

$(blastdb_name).list: $(blastdb_fasta_file)
	grep ">" $(blastdb_fasta_file) | cut -c2- | sed 's/ /\t/' | sort > $(blastdb_name).list

blastdb_clean:	
	-if [ $(blastdb_protein) == "F" ]; then \
		rm $(blastdb_name).n?? ;\
	else \
		rm $(blastdb_name).p?? ;\
	fi
	-rm $(blastdb_name).list
	-rm formatdb.log

