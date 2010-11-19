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

ifneq ($(moa_id)_mode,'simple')

endif
# Help

#########################################################################
#Include moa core
include $(MOABASE)/lib/gnumake/core.mk

ifeq ($($(moa_id)_mode),simple)
$(moa_id)_touch=F
else
$(moa_id)_touch_files=$(addprefix touch/,$(notdir $($(moa_id)_input_files)))
endif

.PHONY: $(moa_id)_prepare
$(moa_id)_prepare:
	$e if [[ "$($(moa_id)_touch)" == "T" ]]; then \
		mkdir touch || true 2>/dev/null; \
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
touch/%: t=$(shell echo '$*' | sed -e '$($(moa_id)_name_sed)')
touch/%: b=$(shell basename $< .$($(moa_id)_input_extension))
touch/%: $($(moa_id)_input_dir)/%
	$(call echo,considering $< -- $t ($b) )
	$(call echo,running $($(moa_id)_process))
	$($(moa_id)_process)
	$e if [[ "$($(moa_id)_touch)" == "T" ]]; then \
		touch $@; \
	fi

endif

################################################################################
## $(moa_id) mode: par
ifeq ($($(moa_id)_mode),par)

$(moa_id): $(moa_id)_check $($(moa_id)_touch_files)

touch/%: t=$(shell echo '$*' | sed -e '$($(moa_id)_name_sed)')
touch/%: b=$(shell basename $< .$($(moa_id)_input_extension))
touch/%: $($(moa_id)_input_dir)/%
	$(call echo,considering $< -- $t)
	$(call warn,running '$($(moa_id)_process)')
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
