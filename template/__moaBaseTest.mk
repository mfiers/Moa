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
## Variables & functions

moa_unittest_var=\
	$(call tstm,Set variable $(1) to '$(2)');\
	moa $(MOA_VERBOSE) set $(1)='$(2)'; \
	grep -qe '^$(1)=$(2)' moa.mk \
		|| (cat moa.mk; $(call exer,Cannot find $(1)=$(2) in moa.mk))

moa_unittest_fileexists==\
		$(call tstm,Check if file $(1) exists);\
		[[ -f "$(1)" ]] \
		|| (ls -l $(1); $(call exer,File $(1) does not exist))

moa_unittest_filenotexists=\
		$(call tstm,Check if file $(1) does not exist);\
		[[ ! -f "$(1)" ]] \
		|| (ls -l $(1); $(call exer,File $(1) exist - should not be there!))

moa_unittest_direxists=\
		$(call tstm,Check if directory $(1) exists);\
		[[ -d "$(1)" ]] \
		|| (ls -l $(1); $(call exer,Directory $(1) does not exist))

moa_unittest_filenotexists=\
		$(call tstm,Check if directory $(1) does not exist);\
		[[ ! -d "$(1)" ]] \
		|| (ls -l $(1); $(call exer,Directory $(1) exist - should not be there!))



################################################################################
## template unit testing

moa_default_unittests += moabase_var

.PHONY: unittest
unittest: unittest_template

.PHONY: unittest_all
unittest_all: base_unittest unittest_template

.PHONY: unittest_template
unittest_template: $(addprefix unittest_template_wrapper_,$(moa_ids))

base_unittest:
	$(e)RANDOMDIR=`mktemp -d`;												\
		$(call warn,Executing base unittest in $$RANDOMDIR);			\
		cd $$RANDOMDIR;													\
		moa new -t 'unittest' test;										\
		moa $(minv) unittests;												\
		if [[ "$$?" != "0" ]]; then 									\
			$(call exer,unittest failed); 								\
		fi;																\
		$(call warn,Finished executing base unittests);					\
		rm -rf $$RANDOMDIR

unittest_template_wrapper_%:
	$(e)RANDOMDIR=`mktemp -d`;											\
		$(call warn,Executing unittest $* in $$RANDOMDIR);			\
		cd $$RANDOMDIR;												\
		moa new -t 'unittest' $*;									\
		moa $(minv) unittest_$* ;							\
		if [[ "$$?" != "0" ]]; then 								\
			$(call exer,unittest failed); 							\
		fi;															\
		$(call warn,Finished executing unittest $*);				\
		rm -rf $$RANDOMDIR