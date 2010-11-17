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

moa_id=r

# Help

#########################################################################
#Include moa core
include $(MOABASE)/lib/gnumake/core.mk
$(moa_id)_touch_files=$(addprefix touch/,$(notdir $($(moa_id)_input_files)))

.PHONY: $(moa_id)_prepare
$(moa_id)_prepare:
	$e if [[ "$($(moa_id)_touch)" == "F" ]]; then \
		rm -rf touch; \
	fi
	mkdir touch || true; \

.PHONY: $(moa_id)_post
$(moa_id)_post:

################################################################################

ifeq ("$(r_input_dir)","")
$(moa_id):    
	$(call warn,No input dir is defined - running the R script witout input files)
	Rscript --vanilla moa.R
else

$(moa_id): $(moa_id)_touch_files

touch/%: $($(moa_id)_input_dir)/%
	$(call echo,Processing $<)
	Rscript --vanilla -f moa.R --args $<
endif

$(moa_id)_unittest:
	-rm -rf 10.input test.*
	mkdir 10.input
	echo 'print ("hello")' > moa.R
	echo -n '1' > 10.input/test.1.input
	echo -n '2' > 10.input/test.2.input
	echo -n '3' > 10.input/test.3.input
	echo -n '4' > 10.input/test.4.input
	echo -n '5' > 10.input/what.5.input
	moa

