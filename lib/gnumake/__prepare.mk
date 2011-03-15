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
###############################################################################
# Preinclude for moabase - optional include for some functions that
# help with defining variables
# If this is not included before the main moabase is included - it will be
# included first thing by Moabase
#
###############################################################################

SHELL := /bin/bash
MOA_INCLUDE_PREPARE = yes

## We use the Gnu Make Standard Library
## See: http://gmsl.sourceforge.net/
include $(MOABASE)/lib/gnumake/util/gmsl

parO:=(
parC:=)


#a colorful mark, showing that this comes from moabase
ifeq ($(MOAANSI),no)
moadebug := DEBUG:
moamark := MOA:
moaerrr := MOAERROR:
moawarn := MOAWARN:
moatest := MOATEST:
else
moadebug := \033[0;41;30mDEBUG\033[0m
moamark := \033[0;42;30mMOA\033[0m
moaerrr := \033[0;1;37;41m!!!\033[0m
moawarn := \033[0;43mWARN\033[0m
moatest := \033[0;42mTEST:\033[0m
endif

echo = (echo -en "$(moawarn)" >&2; echo '$(strip $(1))' >&2)
warn = (echo -en "$(moamark)" >&2; echo '$(strip $(1))' >&2)
tstm = (echo -en "$(moatest)" >&2; echo '$(strip $(1))' >&2)
errr = (echo -en "$(moaerrr)" >&2; echo '$(strip $(1))' >&2)
exer = (echo -en "$(moaerrr)" >&2; echo '$(strip $(1))'"- exiting" >&2; exit -1)
exerUnlock = (( if [[ "$(strip $(1))" ]]; 				\
	then echo -en "$(moaerrr)" >&2; echo '$(strip $(1))' >&2 ; 	\
	fi; 												\
	rm -f moa.runlock || true ); 						\
	exit -1 )

## Define a variable that can be used to hide
## output if the moa/make is not called with the -v flag
ifdef MOA_VERBOSE
e=
minv=-v
mins=
else
e=@
minv=
mins=-s
debug = true
echo = true
endif

################################################################################
## Definition of pre & post targets that can be overridden in the
## local Makefile

.PHONY: moa_preprocess
moa_preprocess:

.PHONY: moa_postprocess
moa_postprocess:

#each analysis MUST have a name
#Variable: set_name

################################################################################
##
## Template loader

moa_load=$(eval include \
	$(if $(wildcard ./.moa/template.d/$(1).mk),\
		./.moa/template.d/$(1).mk,\
		$(error Cannot find a template called $(1))\
	)\
)