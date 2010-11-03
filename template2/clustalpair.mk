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
moa_id = clustalpair

#targets

#variables

include $(MOABASE)/lib/gnumake/core.mk
ix = $(input_extension)
input_files_a = $(addprefix a__,$(wildcard $(input_dir_a)/*.$(input_extension)))
input_files_b = $(wildcard $(input_dir_b)/*.$(input_extension))

.PHONY: clustalpair_prepare
clustalpair_prepare:

.PHONY: clustalpair_post
clustalpair_post:

.PHONY: clustalpair
clustalpair: $(input_files_a)

$(input_files_a): a__%: $(input_files_b)
	@for to in $?; do \
		if [ "$*" == "$$to" ]; then \
			continue ;\
		fi ;\
		$(call echo, clustalling $* against $$to) ;\
		prefix=`basename $* .$(ix)`__`basename $$to .$(ix)` ;\
		cat $* > $$prefix.fasta ;\
		echo >> $$prefix.fasta ;\
		cat $$to >> $$prefix.fasta ;\
		clustalw2 $$prefix.fasta ;\
	done

clean: clustalpair_clean

clustalpair_clean:
	rm -f *.fasta *.aln *.dnd