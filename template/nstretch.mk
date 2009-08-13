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
# Run NStretch
#
# for info: type 
#    make help

################################################################################
# Variable checks & definition & help
moa_ids += nstretch 
moa_title_nstretch = Nstretch
moa_description_nstretch = Run NSTRETCH on an set of input files 

#variables
moa_may_define += nstretch_input_dir
nstretch_input_dir_help = input dir with the fasta files
nstretch_input_dir_cdbattr = fastadir

moa_may_define += nstretch_input_extension
nstretch_input_extension_help = extension of the input files

moa_may_define += nstretch_len
nstretch_len_help = minimal number of Ns before its reported (default 10)

ifndef dont_include_moabase
	include $(shell echo $$MOABASE)/template/moaBase.mk
endif

##### Derived variables for this run
nstretch_input_extension ?= fasta
nstretch_input_dir ?= ./fasta
nstretch_len ?= 10

nstretch_input_files = \
	$(wildcard $(nstretch_input_dir)/*.$(nstretch_input_extension))

nstretch_gff_files = $(addprefix ./gff/, \
  $(patsubst %.$(nstretch_input_extension), %.gff, \
    $(notdir $(nstretch_input_files))))

.PHONY: nstretch_prepare
nstretch_prepare:
	-mkdir gff

.PHONY: nstretch_post
nstretch_post:

nstretch: $(nstretch_gff_files)

./gff/%.gff : $(nstretch_input_dir)/%.$(nstretch_input_extension)
	@echo Processing $*
	@echo Creating gff $@ from $<	
	fastaNfinder $< $(nstretch_len) > $@


nstretch_clean:
	-rm -rf ./gff


