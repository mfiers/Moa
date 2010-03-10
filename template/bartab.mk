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

moa_title = Bartab
moa_description = BARTAB - a tool to process sff files

moa_id = bartab

bartab_help = .. to be written ..


#########################################################################
# Prerequisite testing
moa_prereq_simple += bartab

#########################################################################
## variable definition

moa_must_define += bartab_in
bartab_in_help = input file for bartab
bartab_in_type = file

moa_may_define += bartab_qin
bartab_qin_help = Quality scores for the input fasta file
bartab_qin_type = file

moa_may_define += bartab_map
bartab_map_help = A file mapping barcodes to metadata
bartab_map_type = file
bartab_map_default = 

moa_may_define += bartab_out
bartab_out_help = base output name
bartab_out_type = integer
bartab_out_default = bartab

moa_may_define += bartab_forward_primer
bartab_forward_primer_help = remove forward primer
bartab_forward_primer_type = string
bartab_forward_primer_default = 

moa_may_define += bartab_reverse_primer
bartab_reverse_primer_help = remove reverse primer
bartab_reverse_primer_type = string
bartab_reverse_primer_default = 

moa_may_define += bartab_min_length
bartab_min_length_help = minimun acceptable sequence length
bartab_min_length_type = integer
bartab_min_length_default = 50

moa_may_define += bartab_trim
bartab_trim_help = Trim barcode
bartab_trim_type = set
bartab_trim_default = T
bartab_trim_allowed = T F

#include the moa core libraries
include $(shell echo $$MOABASE)/template/moa/core.mk

.PHONY: bartab_prepare
bartab_prepare:

.PHONY: bartab_post
bartab_post:

.PHONY: bartab_initialize
bartab_initialize:

.PHONY: bartab_clean
bartab_clean:

.PHONY: bartab
bartab:
	$e bartab -in $(bartab_in) \
		$(if $(bartab_qin), -qin $(bartab_qin)) \
		$(if $(bartab_map), -map $(bartab_map)) \
		$(if $(bartab_out), -out $(bartab_out)) \
		$(if $(bartab_forward_primer), -for $(bartab_forward_primer)) \
		$(if $(bartab_reverse_primer), -rev $(bartab_reverse_primer)) \
		$(if $(bartab_min_length), -min $(bartab_min_length)) \
		$(if $(call seq,$(bartab_trim),F),-xbar)

