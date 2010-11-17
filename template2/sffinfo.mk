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
include $(MOABASE)/lib/gnumake/prepare.mk

moa_id = sffinfo

#########################################################################
# Prerequisite testing

#########################################################################
# Variable definition

#include the moa core libraries
include $(MOABASE)/lib/gnumake/core.mk
ifeq ($(sffinfo_accessions),T)

endif

ifeq ($(sffinfo_untrimmed),T)
untrimmed_parameter = -n
else
untrimmed_parameter =
endif

ifeq ($(sffinfo_sequences),T)

endif

ifeq ($(sffinfo_quality),T)

endif

ifeq ($(sffinfo_flowgrams),T)

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