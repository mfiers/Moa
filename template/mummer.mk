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
moa_must_define += input_dir 
moa_may_define += input_extension

include $(shell echo $$MOABASE)/template/moaBase.mk

input_extension ?= fasta
input_files = $(wildcard $(input_dir)/*.$(input_extension))

.PHONY: mummer_prepare
mummer_prepare: 

.PHONY: mummer
mummer: $(input_files)
	for f1 in $^; do \
		for f2 in $^; do \
			echo "considering $$f1 and $$f2 " ;\
			export prefix=`basename $$f1 .$(input_extension)`_`basename $$f2 .$(input_extension)` ;\
			echo "prefix is $$prefix" ;\
			nucmer --prefix=$$prefix $$f1 $$f2 ;\
			show-coords -rcl $$prefix.delta > $$prefix.coords ;\
			mummerplot -t png --large -p $$prefix $$prefix.delta ;\
		done ;\
	done

clean: mummer_clean

mummer_clean:
	-rm *delta