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

$(call moa_fileset_define,adhoc_input,fasta,Input files for adhoc)

# Help
moa_id=adhoc
moa_title_adhoc = Run an ad-hoc analysis
moa_description_adhoc = Run a specified oneliner or script on a set of	\
   inputfiles


moa_may_define += adhoc_name_sed
adhoc_name_sed_default = s/a/a/
adhoc_name_sed_help = SED expression to be executed on each file name -	\
  allows you to change file names
adhoc_name_sed_type = string

moa_may_define += adhoc_output_dir
adhoc_output_dir_default = .
adhoc_output_dir_help = Output subdirectory, defaults to '.'
adhoc_output_dir_type = directory

moa_may_define += adhoc_parallel
adhoc_parallel_default = F
adhoc_parallel_help = allow parallel execution. If, for example,	\
  concatenating to one single file, you should not have multiple	\
  threads.
adhoc_parallel_type = set
adhoc_parallel_allowed = T F

moa_may_define += adhoc_process
adhoc_process_default = ln -f \$< \$t
adhoc_process_help = Command to process the files. If undefined,	\
  hardlink the files.
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

.PHONY: adhoc
adhoc:  $(adhoc_touch_files)

touch/%: t=$(shell echo '$*' | sed $(adhoc_name_sed))
touch/%: $(adhoc_input_dir)/%
	$(call echo,considering $<)
	$e $(adhoc_process)
	touch $@

adhoc_clean: find_exclude_args = \
	$(foreach v, $(adhoc_link_noclean), -not -name $(v))
adhoc_clean: 
	-if [ ! "$(adhoc_output_dir)" == "." ]; then rm -rf $(adhoc_output_dir); fi
	-rm -rf touch
	-if [ "$(adhoc_powerclean)" == "T" ]; then \
		find . -maxdepth 1 -type f $(find_exclude_args) | \
			xargs -n 20 rm -f ; fi