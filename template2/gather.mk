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
moa_id += gather

#varables that NEED to be defined
g_input_dir_cardinality = many

#Include base moa code - does variable checks & generates help
include $(MOABASE)/lib/gnumake/core.mk
#########################################################################

#this is a dummy command, replaces every a with an a - hence nothing happens

gather_link_noclean ?= Makefile moa.mk

.PHONY: gather_link_run

VPATH = $(g_input_dir) 
#vpath %.touch touch/
#vpath % $(g_input_dir)
#vpath %.touch touch/

.PHONY: gather_prepare
gather_prepare:
	-@mkdir touch 2>/dev/null || true
	-@if [[ "$(g_output_dir)" != "." ]]; then 									\
		 mkdir $(g_output_dir);													\
	fi

.PHONY: gather_post
gather_post:

gather_test:
	$e echo '$(addprefix touch/, $(notdir $(foreach dir, $(g_input_dir), \
		$(shell find $(dir)/ -maxdepth 1 -name "$(g_input_pattern)" -printf "%A@\t%p\n" \
		| sort -nr | head -$(g_limit) | cut -f 2 ))))'

ifeq ($(g_parallel),F)
.NOTPARALLEL: gather
endif
.PHONY: gather

gather_input_files = \
	$(foreach dir, $(g_input_dir), $(shell \
		find $(dir)/ -maxdepth 1 -name "$(g_input_pattern)" \
				-printf "%A@\t%p\n" \
			| sort -nr \
			| head -$(g_limit) \
			| cut -f 2 \
			| xargs -n 1 basename \
	))

.PHONY: gather
gather: $(addprefix $(CURDIR)/touch/,$(gather_input_files))

$(CURDIR)/touch/%: g_target=$(shell echo "$(g_output_dir)/$*" | sed $(g_name_sed))
$(CURDIR)/touch/%: %
	$(call echo,gatherer: considering $< - $(g_target))
	$e echo $(g_process)
	$e $(g_process)
	touch $@

gather_clean: find_exclude_args = \
	$(foreach v, $(gather_link_noclean), -not -name $(v))
gather_clean: 
	-if [ ! "$(g_output_dir)" == "." ]; then rm -rf $(g_output_dir); fi
	-rm -rf touch
	-if [ "$(g_powerclean)" == "T" ]; then \
		find . -maxdepth 1 -type f $(find_exclude_args) | \
			xargs -n 20 rm -f ; fi