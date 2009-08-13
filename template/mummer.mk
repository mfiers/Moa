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
##### Main target
maintarget: check mummer

################################################################################
# Variable checks & definition & help
moa_ids += mummer
moa_title_mummer = mummer
moa_description_mummer = Run mummer between two sequences

#targets
moa_targets += mummer clean 
mummer2seq_help = run Mummer

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

.PHONY: mummer_prepare
mummer_prepare:

.PHONY: mummer_post
mummer_post: 

.PHONY: mummer
mummer: $(input_files_a)

$(input_files_a): a__%: $(input_files_b)
	for against in $?; do \
		$(call echo,Comparing $* against $$against) ;\
		prefix=`basename $* .$(ix)`__`basename $$against .$(ix)` ;\
		echo "prefix is $$prefix" ;\
		$(call echo,nucmer --maxmatch --prefix=$$prefix $* $$against) ;\
		nucmer --maxmatch --prefix=$$prefix $* $$against || true ;\
		show-coords -rcl $$prefix.delta > $$prefix.coords || true;\
		mummerplot -R $* -Q $$against --layout -t png -p $$prefix $$prefix.delta || true;\
	done

clean: mummer_clean

mummer_clean:
	-rm *delta *coords *fplot *gp *png *rplot *cluster \
		*.hplot *.ps *.pdf
