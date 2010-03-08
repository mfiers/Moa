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
moa_id = repm

moa_title_repm = Repmfolder
moa_description_repmfolder = Repmfold a set of input files based on a	\
  blast against a reference sequence. This software is written around	\
  bambus

#variables
moa_must_define += repm_input_file
repm_input_file_help = blast database of the reference set
repm_input_file_type = file

moa_may_define += repm_species
repm_species_default = repmfolds
repm_species_help = species 
repm_species_type = string

include $(MOABASE)/template/moa/core.mk

##### Derived variables for this run


.PHONY: repm_prepare
repm_prepare:

.PHONY: repm_post
repm_post:

.PHONY: repm
repm: $(repm_prefix).png

$(repm_prefix).png: $(repm_input_file) $(repm_reference_file)
	repmfolder -v \
		-i $< -r $(repm_reference_file) -p $(repm_prefix)

repm_clean:
	rm -f $(repm_prefix).*

