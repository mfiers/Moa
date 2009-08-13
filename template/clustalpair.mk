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
moa_ids += clustalpair
moa_title_mummer = clustalw
moa_description_mummer = Run clustalw on two sets of sequences

#targets
clustalpair_help = run clustalw

#variables
moa_must_define += input_dir_a input_dir_b
input_dir_a_help= This set is compared to the sequences in input_dir_b. \
  only a forward comparison is made (a against b, not the other way \
  round )
input_dir_b_help= The set to compare against


moa_may_define += input_extension

include $(shell echo $$MOABASE)/template/moaBase.mk

input_extension ?= fasta
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