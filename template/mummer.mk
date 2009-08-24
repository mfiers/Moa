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
moa_must_define += mum_input_dir_a mum_input_dir_b
mum_input_dir_a_help= This set is compared to the sequences in input_dir_b. \
  only a forward comparison is made (a against b, not the other way \
  round )
mum_input_dir_b_help= The set to compare against


moa_may_define += mum_input_extension mum_breaklen
mum_breaklen_help = Set the distance an alignment extension will attempt \
	to extend poor scoring regions before giving up (default 200)

include $(shell echo $$MOABASE)/template/moaBase.mk

ifdef $(input_extension)
	$(error Deprecated variable used)
endif

mum_breaklen ?= 200
mum_input_extension ?= fasta
ix = $(mum_input_extension)
mum_input_files_a = $(addprefix a__, \
		$(wildcard $(mum_input_dir_a)/*.$(mum_input_extension)))
mum_input_files_b = $(wildcard \
		$(mum_input_dir_b)/*.$(mum_input_extension))

.PHONY: mummer_prepare
mummer_prepare:

.PHONY: mummer_post
mummer_post: 

.PHONY: mummer
mummer: $(mum_input_files_a)

$(mum_input_files_a): a__%: $(mum_input_files_b)
	for against in $?; do \
		prefix=`basename $* .$(ix)`__`basename $$against .$(ix)` ;	\
		nucmer --maxmatch -b $(mum_breaklen) --prefix=$$prefix 		\
				$* $$against || true ;	\
		show-coords -rcl $$prefix.delta > $$prefix.coords || true;	\
		mummerplot -R $* -Q $$against --layout 						\
				-t png -p $$prefix $$prefix.delta || true;\
	done

clean: mummer_clean

mummer_clean:
	-rm *delta *coords *fplot *gp *png *rplot *cluster \
		*.hplot *.ps *.pdf *.filter
