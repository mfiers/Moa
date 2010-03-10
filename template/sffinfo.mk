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
# You should have received a copy	 of the GNU General Public License
# along with Moa.  If not, see <http://www.gnu.org/licenses/>.
# 
include $(MOABASE)/template/moa/prepare.mk

moa_title = sffinfo
moa_description = Roche sffinfor tool - extract information from sff files

moa_id = sffinfo

sffinfo_help = Use the Roche sffinfo tool to extract reads, quality	\
scores, flowgrams and accession ids from one or more sff files 

#########################################################################
# Prerequisite testing
moa_prereq_simple += sffinfo

#########################################################################
# Variable definition

$(call moa_fileset_define,sffinfo_input,sff,Sff input files)

moa_may_define += sffinfo_accessions
sffinfo_accessions_help = Output the accessions
sffinfo_accessions_type = set
sffinfo_accessions_default = T
sffinfo_accessions_allowed = T F

moa_may_define += sffinfo_sequences
sffinfo_sequences_help = Output the sequences 
sffinfo_sequences_type = set
sffinfo_sequences_default = T
sffinfo_sequences_allowed = T F

moa_may_define += sffinfo_quality
sffinfo_quality_help = Output quality scores
sffinfo_quality_type = set
sffinfo_quality_default = T
sffinfo_quality_allowed = T F

moa_may_define += sffinfo_flowgrams
sffinfo_flowgrams_help = output the flowgrams
sffinfo_flowgrams_type = set
sffinfo_flowgrams_default = F
sffinfo_flowgrams_allowed = T F

moa_may_define += sffinfo_untrimmed
sffinfo_untrimmed_help = output untrimmed sequences & qualities
sffinfo_untrimmed_type = set
sffinfo_untrimmed_default = F
sffinfo_untrimmed_allowed = T F

#include the moa core libraries
include $(shell echo $$MOABASE)/template/moa/core.mk

ifeq ($(sffinfo_accessions),T)
$(call moa_fileset_remap_nodir,sffinfo_input,sffinfo_accession,acc)
endif

ifeq ($(sffinfo_untrimmed),T)
untrimmed_parameter = -n
else
untrimmed_parameter =
endif

ifeq ($(sffinfo_sequences),T)
$(call moa_fileset_remap_nodir,sffinfo_input,sffinfo_sequence,reads)
endif

ifeq ($(sffinfo_quality),T)
$(call moa_fileset_remap_nodir,sffinfo_input,sffinfo_quality,qual)
endif

ifeq ($(sffinfo_flowgrams),T)
$(call moa_fileset_remap_nodir,sffinfo_input,sffinfo_flowgram,flow)
endif

.PHONY: sffinfo_prepare
sffinfo_prepare:

.PHONY: sffinfo_post
sffinfo_post:

.PHONY: sffinfo_initialize
sffinfo_initialize:

.PHONY: sffinfo_clean
sffinfo_clean:
	-$e rm -f *qual *reads *acc *flow

.PHONY: sffinfo
sffinfo: $(sffinfo_accession_files) \
		$(sffinfo_flowgram_files) \
		$(sffinfo_sequence_files) \
		$(sffinfo_quality_files)

%.reads: $(sffinfo_input_dir)/%.$(sffinfo_input_extension)
	$e sffinfo $(untrimmed_parameter) -s $< > $@

%.qual: $(sffinfo_input_dir)/%.$(sffinfo_input_extension)
	$e sffinfo $(untrimmed_parameter) -q $< > $@

%.flow: $(sffinfo_input_dir)/%.$(sffinfo_input_extension)
	$e sffinfo $(untrimmed_parameter) -f $< > $@

%.acc: $(sffinfo_input_dir)/%.$(sffinfo_input_extension)
	$e sffinfo $(untrimmed_parameter) -a $< > $@