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

################################################################################
# Variable checks & definition & help

include $(shell echo $$MOABASE)/template/moa/prepare.mk

moa_id = mummer
template_title = mummer
template_description = Run mummer between two sequences

#targets
moa_targets += mummer clean 
mummer2seq_help = run Mummer

#variables
$(call moa_fileset_define,mum_input_a,fasta,Set 1 input fasta files)
$(call moa_fileset_define,mum_input_b,fasta,Set 1 input fasta files)

moa_may_define += mum_breaklen
mum_breaklen_help = Set the distance an alignment extension will attempt \
	to extend poor scoring regions before giving up (default 200)
mum_breaklen_default = 200
mum_breaklen_type = integer

moa_may_define += mum_plot_raw
mum_plot_raw_help = plot an alternative visualization where mummer	\
does not attempt to put the sequences in the correct order
mum_plot_raw_type = set
mum_plot_raw_allowed = T F
mum_plot_raw_default = F


moa_may_define += mum_matchmode
mum_matchmode_help = use all matching fragments (max) or only unique matchers (mum)
mum_matchmode_type = set
mum_matchmode_default = mum
mum_matchmode_allowed = mum max

include $(shell echo $$MOABASE)/template/moa/core.mk

mum_a_set = $(addprefix a__, $(mum_input_a_files))
mum_b_set = $(mum_input_b_files)

.PHONY: mummer_prepare
mummer_prepare:

.PHONY: mummer_post
mummer_post: 

mummer_debug:
	@echo $(mum_a_set)
	@echo $(mum_b_set)

.PHONY: mummer
mummer: $(mum_a_set)

aix = $(mum_input_a_extension)
bix = $(mum_input_b_extension)

$(mum_a_set): a__%: $(mum_b_set)
	$e for against in $?; do											\
		if [ "$$against" == "$*" ]; then continue; fi;					\
		prefix=`basename $* .$(aix)`__`basename $$against .$(bix)` ;	\
		nucmer $(if $(call seq,$(mum_matchmode),max),--maxmatch,--mum)  \
			-b $(mum_breaklen) --prefix=$$prefix						\
			$* $$against || true ;										\
		show-coords -rcl $$prefix.delta > $$prefix.coords || true;		\
		mummerplot -R $* -Q $$against --layout --large --color			\
				-t png -p $$prefix $$prefix.delta || true;				\
		mummerplot -R $* -Q $$against --layout	--large --color 		\
				-t postscript -p $$prefix $$prefix.delta || true;		\
		if [[ "$(mum_plot_raw)" == "T" ]]; then							\
			mummerplot -t png -p Raw_$$prefix $$prefix.delta || true;	\
			mummerplot -t postscript -p Raw_$$prefix $$prefix.delta		\
				|| true;												\
			ps2pdf Raw_$$prefix.ps;										\
		fi;																\
	done

clean: mummer_clean

mummer_clean:
	-rm *delta *coords *fplot *gp *png *rplot *cluster \
		*.hplot *.ps *.pdf *.filter
