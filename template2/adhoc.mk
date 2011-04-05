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


#########################################################################
#Include moa core
include $(MOABASE)/lib/gnumake/core.mk

ifeq ($(adhoc_mode),simple)
adhoc_touch=F
else
adhoc_touch_files=$(addprefix touch/,$(notdir $(adhoc_input_files)))
adhoc_input_dir=$(shell dirname $(word 1,$(adhoc_input_files)))

endif

.PHONY: adhoc_prepare
adhoc_prepare:
	$e if [[ "$(adhoc_touch)" == "T" ]]; then \
		(mkdir touch || true) 2>/dev/null; \
	else \
		(rm -rf touch || true) 2>/dev/null; \
	fi
	-$e [[ "$(adhoc_output_dir)" == "." ]] || mkdir $(adhoc_output_dir)

.PHONY: adhoc_post
adhoc_post:


################################################################################
## adhoc mode: seq

ifeq ($(adhoc_mode),seq)

.NOTPARALLEL: adhoc

adhoc:  adhoc_prepare $(adhoc_touch_files)
touch/%: t=$(shell echo '$*' | sed -e '$(adhoc_name_sed)')
touch/%: $(adhoc_input_dir)/%
	$(call echo,considering $< -- $t ($b) )
	$(call echo,running $(adhoc_process))
	$(adhoc_process)
	$e if [[ "$(adhoc_touch)" == "T" ]]; then \
		touch $@; \
	fi
endif

################################################################################
## adhoc mode: par
ifeq ($(adhoc_mode),par)

adhoc:  adhoc_prepare $(adhoc_touch_files)

touch/%: t=$(shell echo '$*' | sed -e '$(adhoc_name_sed)')
touch/%: $(adhoc_input_dir)/%
	$(call echo,considering $< -- $t)
	$(call warn,running '$(adhoc_process)')
	$(adhoc_process)
	$e if [[ "$(adhoc_touch)" == "T" ]]; then \
		touch $@; \
	fi
endif

################################################################################
## adhoc mode: all
ifeq ($(adhoc_mode),all)

adhoc:  adhoc_prepare adhoc_all

adhoc_all: $(adhoc_input_files)
	$(call echo,considering $(words $<) files)
	$(call warn,Running $(adhoc_process))
	$(adhoc_process)

touch/%: $(adhoc_input_dir)/%
	touch $@;
endif

################################################################################
## adhoc mode: simple
ifeq ($(adhoc_mode),simple)
adhoc:
	$(adhoc_process)

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
	-rm -rf 10.input test.*
	mkdir 10.input
	echo -n '1' > 10.input/test.1.input
	echo -n '2' > 10.input/test.2.input
	echo -n '3' > 10.input/test.3.input
	echo -n '4' > 10.input/test.4.input
	echo -n '5' > 10.input/what.5.input
	moa set mode=simple
	moa set process='cat 10.input/* > test.1'
	moa run
	[[ "`cat test.1`" == "12345" ]]
	rm test.1
	moa set mode=seq
	moa set input=10.input/test.*.input
	moa set process='cat $$< >> test.2'
	moa run
	cat test.2
	[[ "`cat test.2`" == "1234" ]]
	rm test.2
	moa set name_sed='s/input/output/'
	moa set process='cat $$< > $$t'
	moa run
	ls
	[[ ! ( -e test.1.output ) ]]
	moa clean
	moa run
	moa show
	ls
	[[ -e test.1.output ]]
	rm test.?.output
	sleep 1
	touch 10.input/test.2.input
	moa run
	[[ -e test.2.output ]]
	[[ ! (-e test.1.output) ]]
