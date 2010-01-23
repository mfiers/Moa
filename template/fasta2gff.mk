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
moa_title = GFF from FASTA
moa_description = Derive GFF from a FASTA file, usually to accompany the 		\
	Sequence for upload to a generic genome browser database.
moa_fasta2gff_help = Generate GFF from a fasta file

# Help
moa_ids += fasta2gff
moa_title_fasta2gff = Fasta to gff
moa_description_fasta2gff = Create gff from a fasta file to accompany upload to \
  a gbrowse db

#varables that NEED to be defined
moa_must_define += f2g_gffsource
f2g_gffsource_help = Source to be used in the gff
f2g_gffsource_type = string

#varables that MAY  be defined
moa_must_define += f2g_input_dir 
f2g_input_dir_help = Directory with the input fasta files
f2g_input_dir_type = directory

moa_may_define += f2g_output_dir
f2g_output_dir_default = ./gff
f2g_output_dir_help = Directory with the output gff 
f2g_output_dir_type = directory

moa_may_define += f2g_input_extension
f2g_input_extension_default = fasta
f2g_input_extension_help = glob pattern of the fasta files (default: *.fasta)
f2g_input_extension_type = string

moa_may_define += f2g_options
f2g_options_default = 
f2g_options_help = options to be passed to the fasta2gff script
f2g_options_type = string

#Include base moa code - does variable checks & generates help
ifndef dont_include_moabase
	include $(shell echo $$MOABASE)/template/moaBase.mk
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