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
moa_id = varscan

#variables

ifndef dont_include_moabase
	include $(shell echo $$MOABASE)/template/moa/core.mk
endif

##### Derived variables for this run

#moa_register_extra += varscan_output
#moa_register_varscanout = $(shell echo `pwd`)/$(varscan_output_name)

.PHONY: varscan_prepare
varscan_prepare:

.PHONY: varscan_post
varscan_post:

.PHONY: varscan
varscan: $(varscan_output_name)
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

