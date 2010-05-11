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

$(call moa_fileset_define_opt,adhoc_input,,Input files for adhoc)

# Help
moa_id=adhoc
template_title = Execute an ad hoc analysis
template_description = The ad hoc template aids in executing a one	\
  line on a set of input files.

moa_may_define += adhoc_touch
adhoc_touch_help = use touch files to track if input files have	\
	changed.
adhoc_touch_type = set
adhoc_touch_default = T
adhoc_touch_allowed = T F

moa_may_define += adhoc_name_sed
adhoc_name_sed_default = s/a/a/
adhoc_name_sed_help = A sed expression which can be used to derive the	\
  output file name for each input file (excluding the path). The sed	\
  expression is executed for each input file name, and the result is	\
  available as $$t in the $$(adhoc_process) statement. Make sure that	\
  you use single quotes when specifying this on the command line
adhoc_name_sed_type = string

moa_may_define += adhoc_output_dir
adhoc_output_dir_default = .
adhoc_output_dir_help = Output subdirectory
adhoc_output_dir_type = directory

moa_may_define += adhoc_mode
adhoc_mode_default = seq
adhoc_mode_help = Adhoc operation mode: *seq*, sequential: process the	\
  input files one by one; *par*, parallel: process the input files in	\
  parallel (use with `-j`); *all*: process all input files at once (use	\
  `$$^` in `adhoc_process`) and *simple*: Ignore input files, just		\
  execute `adhoc_process` once.
adhoc_mode_type = set
adhoc_mode_allowed = seq par all simple

moa_may_define += adhoc_process
adhoc_process_default = echo "need a sensbile command"
adhoc_process_help = Command to execute for each input file. The path	\
  to the input file is available as $$< and the output file as $$t.	\
  (it is not mandatory to use both parameters, for example 				\
"cat $$< > output" would concatenate all files into one big file
adhoc_process_type = string

moa_may_define += adhoc_powerclean
adhoc_powerclean_default = F
adhoc_powerclean_help = Do brute force cleaning (T/F). Remove all		\
  files, except moa.mk & Makefile when calling make clean. Defaults to	\
  F.
adhoc_powerclean_type = set
adhoc_powerclean_allowed = T F

#########################################################################
#Include moa core
include $(MOABASE)/template/moa/core.mk

adhoc_sif:
	@echo $(adhoc_input_files)

ifeq ($(adhoc_mode),simple)
adhoc_touch=F
else
adhoc_touch_files=$(addprefix touch/,$(notdir $(adhoc_input_files)))
endif


adhoc_link_noclean ?= Makefile moa.mk

.PHONY: adhoc_prepare
adhoc_prepare:
	$e if [[ "$(adhoc_touch)" == "T" ]]; then \
		mkdir touch || true; \
	else \
		rm -rf touch || true; \
	fi
	-$e [[ "$(adhoc_output_dir)" == "." ]] || mkdir $(adhoc_output_dir)

.PHONY: adhoc_post
adhoc_post:

## Check if the input_dir is defined
adhoc_check:
	$(if $(adhoc_input_dir),,\
		$(call exerUnlock, Need to define adhoc_input_dir))

################################################################################
## adhoc mode: seq
ifeq ($(adhoc_mode),seq)

.NOTPARALLEL: adhoc

adhoc: adhoc_check $(adhoc_touch_files)

touch/%: t=$(shell echo '$*' | sed $(adhoc_name_sed))
touch/%: $(adhoc_input_dir)/%
	$(call echo,considering $<)
	$e $(adhoc_process)
	$e if [[ "$(adhoc_touch)" == "T" ]]; then \
		touch $@; \
	fi

endif

################################################################################
## adhoc mode: par
ifeq ($(adhoc_mode),par)

adhoc: adhoc_check $(adhoc_touch_files)
		@echo $(adhoc_input_files)

touch/%: t=$(shell echo '$*' | sed $(adhoc_name_sed))
touch/%: $(adhoc_input_dir)/%
	$(call echo,considering $<)
	$e $(adhoc_process)
	$e if [[ "$(adhoc_touch)" == "T" ]]; then \
		touch $@; \
	fi

endif

################################################################################
## adhoc mode: all
ifeq ($(adhoc_mode),all)

adhoc: adhoc_check adhoc_all

adhoc_all: $(adhoc_input_files)
	$(call echo,considering $(words $^) files)
	$e $(adhoc_process)

endif


################################################################################
## adhoc mode: all
ifeq ($(adhoc_mode),simple)

adhoc: 
	$(call echo,Running adhoc without input files)
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


adhoc_unittest:
	mkdir 10.input
	echo -n '1' > 10.input/test.1.input
	echo -n '2' > 10.input/test.2.input
	echo -n '3' > 10.input/test.3.input
	echo -n '4' > 10.input/test.4.input
	echo -n '5' > 10.input/what.5.input
	moa set adhoc_mode=simple
	moa set adhoc_process='cat 10.input/* > test.1'
	moa
	cat test.1
	[[ "`cat test.1`" == "12345" ]]
	rm test.1
	moa set adhoc_mode=seq
	moa set adhoc_input_dir=10.input
	moa set adhoc_input_extensions=input
	moa set adhoc_input_glob=test.*
	moa set adhoc_process='cat $$< >> test.2'
	moa
	cat test.2
	[[ "`cat test.2`" == "1234" ]]
	rm test.2
	moa set adhoc_name_sed='s/input/output/'
	moa set adhoc_process='cat $$< > $$t'
	moa
	ls
	[[ ! (-e test.1.output) ]]
	moa clean
	moa
	moa show
	ls
	[[ -e test.1.output ]]
	rm test.?.output
	touch 10.input/test.2.input
	moa
	[[ -e test.2.output ]]
	[[ ! (-e test.1.output) ]]
	moa set adhoc_touch=F
	rm test.?.output
	moa -v
	ls
	[[  (-e test.1.output) ]]
	moa set adhoc_touch=T
