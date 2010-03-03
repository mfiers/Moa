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
MOA_INCLUDED_PREPARE = yes

## We use the Gnu Make Standard Library
## See: http://gmsl.sourceforge.net/
include $(MOABASE)/template/gmsl

## Files that moa uses
moa_system_files = Makefile moa.mk moa.archive 


## some help variables
warn_on := \033[0;41;37m
warn_off := \033[0m
boldOn := \033[0;1;47;0;32;4m
boldOff := \033[0m

#a colorful mark, showing that this comes from moabase
ifeq ($(MOAANSI),no)
moamark := MOA:
moaerrr := MOAERROR:
moawarn := MOAWARN:
moatest := MOATEST:
else
moamark := \033[0;42;30mm\033[0m
moaerrr := \033[0;1;37;41m!!!\033[0m
moawarn := \033[0;43m>>\033[0m
moatest := \033[0;42mTEST:\033[0m
endif
echo = echo -e "$(moamark) $(strip $(1))"
warn = echo -e "$(moawarn) $(strip $(1))"
tstm = echo -e "$(moatest) $(strip $(1))"
errr = echo -e "$(moaerrr) $(strip $(1))"
exer = echo -e "$(moaerrr) $(1) - exiting"; exit -1
exerUnlock = ( if [[ "$(strip $(1))" ]]; 		\
	then echo -e "$(moaerrr) $(strip $(1))"; 	\
	fi; 										\
	rm -f moa.runlock || true ); 				\
	exit -1 

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
endif

moa_fileset_define = \
	$(eval moa_must_define += $(1)_dir) \
	$(eval moa_may_define += $(1)_extension) \
	$(eval moa_may_define += $(1)_glob) \
	$(eval $(1)_dir_help = $(3)) \
	$(eval $(1)_dir_type = directory) \
	$(eval $(1)_extension_help = file extension for the files in $(1)_dir) \
	$(eval $(1)_extension_type = string) \
	$(eval $(1)_extension_default = $(2)) \
	$(eval $(1)_glob_help = glob to select a subset of files from $(1)_dir) \
	$(eval $(1)_glob_type = string) \
	$(eval $(1)_glob_default=*) \
	$(eval _moa_filesets += $(1))



################################################################################
## Some python tricks
##

exec_python = $(eval export $(1)) \
echo "$$$(strip $(1))" | python
