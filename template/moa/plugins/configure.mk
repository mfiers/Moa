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

################################################################################
## configure ###################################################################
#
####  Set parameters
#
################################################################################

set_help = set a variable to moa.mk

#the actual set routine is handled by the moa-python code

moa_pre_set: $(moa_hooks_preset) 

moa_post_set: $(moa_hooks_postset)

#moa_set_2:#
#	moa $(minv) __set $(value MOAARGS)

.PHONY: moa_plugin_configure_test
moa_plugin_configure_test:
	$e moa set title=test
	moa show | grep -P "title\s+test" || \
		($(call exer,set title=VALUE did not work))
	$e moa set title+=two
	$e moa show | grep -P "title\s+test two" || \
		($(call exer,set title+=VALUE does not work))
	$e moa set title=
	$e moa show | grep -P "^title\s*$$" \
		&& ($(call exer,unset title does not work)) \
		|| true;
