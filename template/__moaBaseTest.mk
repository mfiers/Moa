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

MOA_INCLUDE_TEST = yup

################################################################################
## template unit testing

.PHONY: unittest
unittest: $(addprefix unittest_wrapper_,$(moa_ids))

moa_unittest_var=moa -vv set $(1)='$(2)'; \
	grep -e '^$(1)=$(2)' moa.mk \
		|| (cat moa.mk; $(call exer,Cannot find $(1)=$(2) in moa.mk))

moa_unittest_fileexists=[[ -f "$(1)" ]] \
		|| (ls -l $(1); $(call exer,File $(1) does not exist))

moa_unittest_filenotexists=[[ ! -f "$(1)" ]] \
		|| (ls -l $(1); $(call exer,File $(1) exist - should not be there!))

moa_unittest_direxists=[[ -d "$(1)" ]] \
		|| (ls -l $(1); $(call exer,Directory $(1) does not exist))

moa_unittest_filenotexists=[[ ! -d "$(1)" ]] \
		|| (ls -l $(1); $(call exer,Directory $(1) exist - should not be there!))

unittest_wrapper_%:
	RANDOMDIR=`mktemp -d`;											\
		$(call warn,Executing unittest $* in $$RANDOMDIR);			\
		cd $$RANDOMDIR;												\
		moa new -t 'unittest' $*;									\
		moa -v unittest_$* ;										\
		if [[ "$$?" != "0" ]]; then \
			$(call exer,unittest failed); \
		fi;	\
		$(call warn,Finished executing unittest $*);				\
		rm -rf $$RANDOMDIR
