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
moa_ids += varscan 
moa_title_varscan = Varscan
moa_description_varscan = Run VARSCAN to detect snps

#variables
moa_must_define += varscan_input_file
varscan_input_file_help = Varscan input alignments file
varscan_input_file_type = file

moa_may_define += varscan_extra_params
varscan_extra_params_default = 
varscan_extra_params_help = location of varscan.pl, defaults to '/usr/lib/perl5/site_perl/5.8.8/varscan.pl'
varscan_extra_params_type = string

moa_may_define += varscan_output_name
varscan_output_name_default = out
varscan_output_name_help = Base name of the output files
varscan_output_name_type = string

moa_may_define += varscan_perl_file
varscan_perl_file_default = 
varscan_perl_file_help = the varscan (perl) executable
varscan_perl_file_type = file

ifndef dont_include_moabase
	include $(shell echo $$MOABASE)/template/moaBase.mk
endif

##### Derived variables for this run

#moa_register_extra += varscan_output
#moa_register_varscanout = $(shell echo `pwd`)/$(varscan_output_name)

.PHONY: varscan_prepare
varscan_prepare:

.PHONY: varscan_post
varscan_post: 

.PHONY: varscan
varscan:
	perl $(varscan_perl_file) easyrun \
		$(varscan_input_file) \
		--sample $(varscan_output_name)

$(varscan_output_name): $(varscan_input_files)
	varscan $(varscan_input_format_param) \
		-p $(MOA_PROCESSORS) \
		$(varscan_extra_params) \
		$(varscan_db) \
		$(call merge,$(comma),$^) \
		output

varscan_clean:
	-rm -f $(varscan_output_name)

