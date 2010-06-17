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
include $(MOABASE)/template/util/gmsl

## Load moa system wide configuration
MOA_INCLUDE_ETCMOACONF = yes
include $(MOABASE)/etc/moa.conf.mk

## Load user specific configuration
-include ~/.moa/moa.conf.mk

## Load moa project wide configuration
ifdef MOAPROJECTROOT
	MOA_INCLUDE_PROJECTCONF = yes
	-include $(MOAPROJECTROOT)/moa.mk
endif

## Load the local configuration
MOA_INCLUDE_MOAMK = yes
-include moa.mk

## Load plugins early - load before template definitions are made
$(foreach p,$(moa_plugins), \
	$(eval -include $(MOABASE)/template/moa/plugins/$(p)_def.mk) \
)

## Files that moa recognizes
moa_system_files = Makefile moa.mk

## some help variables
warn_on := \033[0;41;37m
warn_off := \033[0m
boldOn := \033[0;1;47;0;32;4m
boldOff := \033[0m

empty:=
space:= $(empty) $(empty)
comma:=,
sep:=|
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
moawarn := \033[0;43m>>\033[0m
moatest := \033[0;42mTEST:\033[0m
endif

warn = (echo -e "$(moawarn)$(strip $(1))" 1>&2)
tstm = (echo -e "$(moatest)$(strip $(1))" 1>&2)
errr = (echo -e "$(moaerrr)$(strip $(1))" 1>&2)
exer = (echo -e "$(moaerrr)$(strip $(1)) - exiting"  1>&2; exit -1)
exerUnlock = (( if [[ "$(strip $(1))" ]]; 				\
	then echo -e "$(moaerrr)"'$(strip $(1))' 1>&2 ; 	\
	fi; 												\
	rm -f moa.runlock || true ); 						\
	exit -1 )

## Define a variable that can be used to hide
## output if the moa/make is not called with the -v flag
ifdef MOA_VERBOSE
e=
minv=-v
mins=
debug = echo -e "$(moadebug) $(strip $(1))"
echo = echo -e "$(moamark) $(strip $(1))"
else
e=@
minv=
mins=-s
debug = true
echo = true
endif


################################################################################
## Some python tricks
##

exec_python = $(eval export $(1)) \
echo "$$$(strip $(1))" | python


################################################################################
## Definition of pre & post targets that can be overridden in the
## local Makefile

.PHONY: moa_preprocess
moa_preprocess:

.PHONY: moa_postprocess
moa_postprocess:

#each analysis MUST have a name
#Variable: set_name
#moa_may_define += project
moa_must_define += title
title_type = string
title_help = A name for this job
title_category = system

# moa_may_define += description
# description_type = string
# description_help = A longer description for this job
# description_default = 
# description_category = system

## author of this template..
template_author ?= Mark Fiers

## aditional  pre/post process command - to be definable in moa.mk
## this is only one single command.
moa_may_define += moa_precommand
moa_precommand_help = A single command to be executed before the main		\
  operation starts. For more complicated processing, please override the	\
  moa_preprocess target in the local Makefile.
moa_precommand_default=
moa_precommand_type = string
moa_precommand_category = advanced

moa_may_define += moa_postcommand
moa_postcommand_help = A single shell command to be executed after the			\
Moa is finished. For more complex processing please override the				\
moa_postprocess target in the local Makefile.
moa_postcommand_category = advanced
moa_postcommand_type = string
moa_postcommand_default=

################################################################################
##
## Template loader

moa_load=$(eval include \
	$(if $(wildcard ~/.moa/template/$(1).mk),\
		~/.moa/template/$(1).mk,\
		$(if $(wildcard $(MOABASE)/template/$(1).mk),\
			$(MOABASE)/template/$(1).mk,\
			$(error Cannot find a template called $(1))\
		)\
	))