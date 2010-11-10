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
moa_id = clustalgroup

#targets

#variables

include $(MOABASE)/lib/gnumake/core.mk
cwg_input_files = $(wildcard $(cwg_input_dir)/*.$(cwg_input_extension))

.PHONY: clustalgroup_prepare
clustalgroup_prepare:

.PHONY: clustalgroup_post
clustalgroup_post:

.PHONY: clustalgroup
clustalgroup: $(cwg_input_files)
	-rm clustal.fasta
	for f in $^; do \
		cat $$f >> clustal.fasta ;\
		echo >> clustal.fasta ;\
	done
	clustalw2 clustal.fasta ;\

clustalgroup_clean:
