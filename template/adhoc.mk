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
adhoc_help = adhoc files

dol:=$

$(call moa_fileset_define,adhoc_input,,Input files for adhoc)

# Help
moa_id=adhoc
template_title = Execute an ad hoc analysis
template_description = The ad hoc template aids in executing a one	\
  line on a set of input files.

moa_may_define += adhoc_name_sed
adhoc_name_sed_default = s/a/a/
adhoc_name_sed_help = A sed expression which can be used to derive the	\
output file name for each input file (excluding the path). The sed		\
expression is executed for each input file name, and the result is		\
available as $$t in the $$(adhoc_process) statement. Make sure that		\
you use single quotes when specifying this on the command line

adhoc_name_sed_type = string

moa_may_define += adhoc_output_dir
adhoc_output_dir_default = .
adhoc_output_dir_help = Output subdirectory
adhoc_output_dir_type = directory

moa_may_define += adhoc_parallel
adhoc_parallel_default = F
adhoc_parallel_help = Allow parallel execution. Use with care (for		\
example when concatenating many files into one big one). You can use	\
the -j parameter to specify the number of threads
adhoc_parallel_type = set
adhoc_parallel_allowed = T F

moa_may_define += adhoc_process
adhoc_process_default = ln -f $$< $$t
adhoc_process_help = Command to execute for each input file. The path	\
to the input file is available as $$< and the output file as $$t.	\
(it is not mandatory to use both parameters, for example 				\
"cat $$< > output" would concatenate all files into one big file
adhoc_process_type = string

moa_may_define += adhoc_limit
adhoc_limit_default = 1000000
adhoc_limit_help = limit the number of files adhoced (with the most	\
  recent files first, defaults to 1mln)
adhoc_limit_type = integer

moa_may_define += adhoc_powerclean
adhoc_powerclean_default = F
adhoc_powerclean_help = Do brute force cleaning (T/F). Remove all		\
  files, except moa.mk & Makefile when calling make clean. Defaults to	\
  F.
adhoc_powerclean_type = set
adhoc_powerclean_allowed = T F

moa_may_define += adhoc_combine
adhoc_combine_help = Use all input files at once (Note, use $$^ (all	\
input files) or $$@ (newer input files) instead of $$<)
adhoc_combine_type = set
adhoc_combine_default = F
adhoc_combine_allowed = T F


#########################################################################
#Include base moa code - does variable checks & generates help
include $(shell echo $$MOABASE)/template/moa/core.mk

adhoc_touch_files=$(addprefix touch/,$(notdir $(adhoc_input_files)))

adhoc_link_noclean ?= Makefile moa.mk

.PHONY: adhoc_prepare
adhoc_prepare:
	-$e mkdir touch 2>/dev/null || true
	-$e [[ "$(adhoc_output_dir)" == "." ]] || mkdir $(adhoc_output_dir)

.PHONY: adhoc_post
adhoc_post:

ifeq ($(adhoc_parallel),F)
.NOTPARALLEL: adhoc
endif

.PHONY: adhoc
ifeq ($(adhoc_combine),F)

adhoc:  $(adhoc_touch_files)

touch/%: t=$(shell echo '$*' | sed $(adhoc_name_sed))
touch/%: $(adhoc_input_dir)/%
	$(call echo,considering $<)
	$e $(adhoc_process)
	touch $@
else

adhoc: $(adhoc_input_files)
	$(call warn,execuing $(words $^) input file(s) at once)
	$e $(adhoc_process)

endif

adhoc_clean: find_exclude_args = \
	$(foreach v, $(adhoc_link_noclean), -not -name $(v))
adhoc_clean: 
	-if [ ! "$(adhoc_output_dir)" == "." ]; then rm -rf $(adhoc_output_dir); fi
	-rm -rf touch
	-if [ "$(adhoc_powerclean)" == "T" ]; then \
		find . -maxdepth 1 -type f $(find_exclude_args) | \
			xargs -n 20 rm -f ; fi