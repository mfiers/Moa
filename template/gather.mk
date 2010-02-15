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
gather_help = gather files
clean_help = Remove anything that is not called Makefile or moa.mk 

# Help
moa_ids += gather
moa_title_gather = gather files
moa_description_gather = gather a set of files and create hardlinks				\
 to. Hardlinks have as advantage that updates are noticed via the				\
 timestamp. Hence, make recognizes them.

#varables that NEED to be defined
moa_must_define += g_input_dir
g_input_dir_help = list of directories with the input files
g_input_dir_type = directory
g_input_dir_cardinality = many

moa_may_define += g_input_pattern
g_input_pattern_default = *
g_input_pattern_help = glob pattern to download
g_input_pattern_type = string

moa_may_define += g_name_sed
g_name_sed_default = s/a/a/
g_name_sed_help = SED expression to be executed on each file name - allows you to \
  change file names
g_name_sed_type = string

name_sed_help = Sed substitution command that alters the filename,				\
  defaults to leaving the names untouched.

moa_may_define += g_output_dir
g_output_dir_default = .
g_output_dir_help = Output subdirectory, defaults to '.'
g_output_dir_type = directory

moa_may_define += g_parallel
g_parallel_default = F
g_parallel_help = allow parallel execution (T) or not (**F**). If for example\
  concatenating to one single file, you should not have multiple threads.
g_parallel_type = set

g_parallel_allowed = T F

moa_may_define += g_process
g_process_default = ln -f $$< $$(g_target)
g_process_help = Command to process the files. If undefined, hardlink the files.
g_process_type = string

moa_may_define += g_limit
g_limit_default = 1000000
g_limit_help = limit the number of files gathered (with the most recent files first, defaults to 1mln)
g_limit_type = integer

moa_may_define += g_powerclean
g_powerclean_default = F
g_powerclean_help = Do brute force cleaning (T/F). Remove all files, except moa.mk & Makefile when calling make clean. Defaults to F.
g_powerclean_type = set

g_powerclean_allowed = T F

#Include base moa code - does variable checks & generates help
include $(shell echo $$MOABASE)/template/moaBase.mk

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