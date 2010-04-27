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
moa_id = scaf

template_title = Scaffolder
template_description = Scaffold a set of input files based on a	\
  blast against a reference sequence. This software is written around	\
  bambus

#variables
moa_must_define += scaf_reference_file
scaf_reference_file_help = blast database of the reference set
scaf_reference_file_type = file

moa_must_define += scaf_input_file
scaf_input_file_help = input file with the sequences to scaffold
scaf_input_file_type = file

moa_may_define += scaf_prefix
scaf_prefix_default = scaffolds
scaf_prefix_help = prefix for scaffolding output files
scaf_prefix_type = string

include $(MOABASE)/template/moa/core.mk

##### Derived variables for this run


.PHONY: scaf_prepare
scaf_prepare:

.PHONY: scaf_post
scaf_post:

.PHONY: scaf
scaf: $(scaf_prefix).png

$(scaf_prefix).png: $(scaf_input_file) $(scaf_reference_file)
	scaffolder -v \
		-i $< -r $(scaf_reference_file) -p $(scaf_prefix)

scaf_clean:
	rm -f $(scaf_prefix).*
	rm -f goBambus.*
	rm -f formatdb.log

