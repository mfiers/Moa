#
#    Copyright 2009 Mark Fiers
#
#    This file is part of Moa 
#
#    Moa is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Moa is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Moa.  If not, see <http://www.gnu.org/licenses/>.
#
#    See: http://github.com/mfiers/Moa/
#
# Run Mummer between two sequences
#
#
################################################################################
# Variable checks & definition & help
moa_ids += clustalgroup
moa_title_mummer = clustalw
moa_description_mummer = Run clustalw on two sets of sequences

#targets
clustalgroup_help = run clustalw

#variables
moa_must_define += cwg_input_dir
cwg_input_dir_help= This set of sequences to run clustalw on


moa_may_define += cwg_input_extension

include $(shell echo $$MOABASE)/template/moaBase.mk

cwg_input_extension ?= fasta
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
