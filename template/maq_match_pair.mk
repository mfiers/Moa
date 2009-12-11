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

ifndef dont_include_moabase
	include $(shell echo $$MOABASE)/template/moaBasePre.mk
endif

moa_ids += maqpair
moa_title_maq_fasta2bfa = MAQ paired ends mapper
moa_description_maq_fasta2bfa = Map paired ends to a reference	\
sequence using MAQ

#variables
moa_must_define += maqpair_read_dir
maqpair_read_dir_help = directory containing the forward reads
maqpair_read_dir_type = string

moa_must_define += maqpair_forward_suffix
maqpair_forward_suffix_help = Suffix of each forward filename -	\
  recognize forward files this way. Note this is not a regular \
  extension, no '.' is assumed between the filename & suffix
maqpair_forward_suffix_default = _f.bfq
maqpair_forward_suffix_type = string

moa_may_define += maqpair_reverse_suffix
maqpair_reverse_suffix_help = suffix of reverse files
maqpair_reverse_suffix_default=_r.bfq
maqpair_reverse_suffix_type = string

moa_must_define += maqpair_reference
maqpair_reference_help = Reference bfa file to map the reads to 
maqpair_reference_type = string

moa_may_define += maqpair_RF_maxdist
maqpair_RF_maxdist_help = max outer distance for an RF readpair	\
(corresponds to the -A parameter). This applies to long insert illumina pairs
maqpair_RF_maxdist_type = integer
maqpair_RF_maxdist_default = 15000


moa_may_define += maqpair_maxdist
maqpair_maxdist_help = max outer distance for a (non RF)			\
readpair. This applies to illumina matepairs - i.e. short inserts
maqpair_maxdist_type = integer
maqpair_maxdist_default = 250


ifndef dont_include_moabase
	include $(shell echo $$MOABASE)/template/moaBase.mk
endif

##### Derived variables for this run

forward_files = $(wildcard $(maqpair_read_dir)/*$(maqpair_forward_suffix))
maqpair_outfiles = $(addsuffix .out,\
		$(patsubst %$(maqpair_forward_suffix),%,$(notdir $(forward_files))))

test:
	@echo $(forward_files)
	$e echo
	@echo $(maqpair_outfiles)

.PHONY: maqpair_prepare
maqpair_prepare:

.PHONY: maqpair_post
maqpair_post:

maqpair: $(maqpair_outfiles)

$(maqpair_outfiles): %.out : \
	$(maqpair_reference) \
	$(maqpair_read_dir)/%$(maqpair_forward_suffix) \
	$(maqpair_read_dir)/%$(maqpair_reverse_suffix)
	$e maq map -A $(maqpair_RF_maxdist) -a $(maqpair_maxdist) $@ $?

bfq/%.bfq: $(maqpair_input_dir)/%.$(maqpair_input_extension)
	maq fastq2bfq $< $@

maqpair_clean:
	$e -rm -rf *.out





