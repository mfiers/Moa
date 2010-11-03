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

# Help
moa_id = fasta2gff

#varables that NEED to be defined

#varables that MAY  be defined

#Include base moa code - does variable checks & generates help
ifndef dont_include_moabase
	include $(shell echo $$MOABASE)/template/moa/core.mk
endif

################################################################################

f2g_input_files = $(wildcard $(f2g_input_dir)/*.$(f2g_input_extension))
f2g_output_files = \
    $(addprefix $(f2g_output_dir)/, \
        $(patsubst %.$(f2g_input_extension), %.gff, \
            $(notdir $(f2g_input_files) )\
        )\
     )

#if we;re going to upload this, prepare gff upload
gup_gffsource ?= $(f2g_gffsource)
gup_upload_fasta ?= T
gup_upload_gff ?= T

.PHONY: fasta2gff_prepare
fasta2gff_prepare:
	-@if [ ! "$(f2g_output_dir)" == "." ]; then \
		mkdir $(f2g_output_dir) ;\
	fi

#rerun make, make sure all files are recognized
.PHONY: fasta2gff
fasta2gff: 
	$(MAKE) fasta2gff2

.PHONY: fasta2gff2
fasta2gff2: $(f2g_output_files)
	@echo fasta2gff2 - done

$(f2g_output_files): $(f2g_output_dir)/%.gff : $(f2g_input_dir)/%.$(f2g_input_extension)
	fasta2gff $< -s $(f2g_gffsource) $(f2g_options) > $@

.PHONY: fasta2gff_post
fasta2gff_post:

.PHONY: fasta2gff_clean
fasta2gff_clean:
	-@if [ ! "$(f2g_output_dir)" == "." ]; then \
		rm -rf $(f2g_output_dir) ;\
	fi