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

moa_id=adhoc

$(call moa_fileset_define_opt,$(moa_id)_input,,Input files for $(moa_id))

# Help

template_title = Execute an ad hoc analysis
template_description = The ad hoc template aids in executing a one	\
  line on a set of input files.

moa_may_define += $(moa_id)_touch
$(moa_id)_touch_help = use touch files to track if input files have	\
	changed.
$(moa_id)_touch_type = set
$(moa_id)_touch_default = T
$(moa_id)_touch_allowed = T F

moa_may_define += $(moa_id)_name_sed
$(moa_id)_name_sed_default = s/a/a/
$(moa_id)_name_sed_help = A sed expression which can be used to derive the	\
  output file name for each input file (excluding the path). The sed	\
  expression is executed for each input file name, and the result is	\
  available as $$t in the $$($(moa_id)_process) statement. Make sure that	\
  you use single quotes when specifying this on the command line
$(moa_id)_name_sed_type = string

moa_may_define += $(moa_id)_r_mode
$(moa_id)_r_mode_help = R mode is a dedication mode to run R scripts 
$(moa_id)_r_mode_type = set
$(moa_id)_r_mode_default = F
$(moa_id)_r_mode_allowed = T F

moa_may_define += $(moa_id)_output_dir
$(moa_id)_output_dir_default = .
$(moa_id)_output_dir_help = Output subdirectory
$(moa_id)_output_dir_type = directory

moa_may_define += $(moa_id)_mode
$(moa_id)_mode_default = seq
$(moa_id)_mode_help = $(Moa_Id) operation mode: *seq*, sequential: process the	\
  input files one by one; *par*, parallel: process the input files in	\
  parallel (use with `-j`); *all*: process all input files at once (use	\
  `$$^` in `$(moa_id)_process`) and *simple*: Ignore input files, just		\
  execute `$(moa_id)_process` once.
$(moa_id)_mode_type = set
$(moa_id)_mode_allowed = seq par all simple

moa_may_define += $(moa_id)_process
$(moa_id)_process_default = echo "needs a sensbile command"
$(moa_id)_process_help = Command to execute for each input file. The path	\
  to the input file is available as $$< and the output file as $$t.	\
  (it is not mandatory to use both parameters, for example 				\
"cat $$< > output" would concatenate all files into one big file
$(moa_id)_process_type = string

moa_may_define += $(moa_id)_powerclean
$(moa_id)_powerclean_default = F
$(moa_id)_powerclean_help = Do brute force cleaning (T/F). Remove all		\
  files, except moa.mk & Makefile when calling make clean. Defaults to	\
  F.
$(moa_id)_powerclean_type = set
$(moa_id)_powerclean_allowed = T F

#########################################################################
#Include moa core
include $(MOABASE)/template/moa/core.mk

ifeq ($($(moa_id)_mode),simple)
$(moa_id)_touch=F
else
$(moa_id)_touch_files=$(addprefix touch/,$(notdir $($(moa_id)_input_files)))
endif


ifeq ($($(moa_id)_r_mode),T)
ifeq ($($(moa_id)_process),$($(moa_id)_process_default))
ifeq ($($(moa_id)_mode),all)
$(moa_id)_process=Rscript --vanilla moa.R --args $^ 
else
ifeq ($($(moa_id)_mode),simple)
$(moa_id)_process=Rscript --vanilla moa.R
else
$(moa_id)_process=Rscript --vanilla moa.R --args $< > $t
endif
endif
endif
endif


$(moa_id)_link_noclean ?= Makefile moa.mk

.PHONY: $(moa_id)_prepare
$(moa_id)_prepare:
	$e if [[ "$($(moa_id)_touch)" == "T" ]]; then \
		mkdir touch || true; \
	else \
		rm -rf touch || true; \
	fi
	-$e [[ "$($(moa_id)_output_dir)" == "." ]] || mkdir $($(moa_id)_output_dir)

.PHONY: $(moa_id)_post
$(moa_id)_post:

## Check if the input_dir is defined
$(moa_id)_check:
	$(if $($(moa_id)_input_dir),,\
		$(call exerUnlock, Need to define $(moa_id)_input_dir))

################################################################################
## $(moa_id) mode: seq
ifeq ($($(moa_id)_mode),seq)

.NOTPARALLEL: $(moa_id)

$(moa_id): $(moa_id)_check $($(moa_id)_touch_files)

touch/%: t=$(shell echo '$*' | sed $($(moa_id)_name_sed))
touch/%: $($(moa_id)_input_dir)/%
	$(call echo,considering $<)
	$(call warn,running '$($(moa_id)_process)')
	$($(moa_id)_process)
	$e if [[ "$($(moa_id)_touch)" == "T" ]]; then \
		touch $@; \
	fi

endif

################################################################################
## $(moa_id) mode: par
ifeq ($($(moa_id)_mode),par)

$(moa_id): $(moa_id)_check $($(moa_id)_touch_files)

touch/%: t=$(shell echo '$*' | sed $($(moa_id)_name_sed))
touch/%: $($(moa_id)_input_dir)/%
	$(call echo,considering $<)
	$($(moa_id)_process)
	$e if [[ "$($(moa_id)_touch)" == "T" ]]; then \
		touch $@; \
	fi

endif

################################################################################
## $(moa_id) mode: all
ifeq ($($(moa_id)_mode),all)

$(moa_id):  $(moa_id)_check $(moa_id)_all

$(moa_id)_all: $($(moa_id)_input_files)
	$(call echo,considering $(words $<) files)
	$(call warn,Running $($(moa_id)_process))
	$($(moa_id)_process)

touch/%: $($(moa_id)_input_dir)/%
	touch $@;
endif


################################################################################
## $(moa_id) mode: simple
ifeq ($($(moa_id)_mode),simple)

$(moa_id):
	$(call echo,Running $(moa_id) without input files)
	$($(moa_id)_process)
endif

$(moa_id)_clean: find_exclude_args = \
	$(foreach v, $($(moa_id)_link_noclean), -not -name $(v))

$(moa_id)_clean: 
	-if [ ! "$($(moa_id)_output_dir)" == "." ]; then rm -rf $($(moa_id)_output_dir); fi
	-rm -rf touch
	-if [ "$($(moa_id)_powerclean)" == "T" ]; then \
		find . -maxdepth 1 -type f $(find_exclude_args) | \
			xargs -n 20 rm -f ; fi


$(moa_id)_unittest:
	-rm -rf 10.input test.*
	mkdir 10.input
	echo -n '1' > 10.input/test.1.input
	echo -n '2' > 10.input/test.2.input
	echo -n '3' > 10.input/test.3.input
	echo -n '4' > 10.input/test.4.input
	echo -n '5' > 10.input/what.5.input
	moa set $(moa_id)_mode=simple
	moa set $(moa_id)_process='cat 10.input/* > test.1'
	moa
	#cat test.1
	[[ "`cat test.1`" == "12345" ]]
	rm test.1
	moa set $(moa_id)_mode=seq
	moa set $(moa_id)_input_dir=10.input
	moa set $(moa_id)_input_extensions=input
	moa set $(moa_id)_input_glob=test.*
	moa set $(moa_id)_process='cat $$< >> test.2'
	moa
	#cat test.2
	[[ "`cat test.2`" == "2341" ]]
	rm test.2
	moa set $(moa_id)_name_sed='s/input/output/'
	moa set $(moa_id)_process='cat $$< > $$t'
	moa
	ls
	[[ ! ( -e test.1.output ) ]]
	moa clean
	moa
	moa show
	ls
	[[ -e test.1.output ]]
	rm test.?.output
	sleep 1
	touch 10.input/test.2.input
	moa
	[[ -e test.2.output ]]
	[[ ! (-e test.1.output) ]]
	moa set $(moa_id)_touch=F
	rm test.?.output
	moa -v
	ls
	[[  (-e test.1.output) ]]
	moa set $(moa_id)_touch=T
