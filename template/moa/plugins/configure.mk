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

#moa_pre_set: $(moa_hooks_preset) 
#moa_post_set: $(moa_hooks_postset)

#moa_set_2:#
#	moa $(minv) __set $(value MOAARGS)

.PHONY: moa_plugin_configure_test
moa_plugin_configure_test:

#return variables as interpreted by Gnu Make
################################################################################
## make show ###################################################################
#
#### Show the current variables from moa.mk
#
################################################################################

sq='
#"' <- to satifsy emacs :(
backslash=\$(empty)
.PHONY: moa_show
moa_show:
	$e echo -n
	$e $(foreach var,$(moa_must_define) $(moa_may_define), \
		echo -ne "$(var)\t"; \
		echo '$(subst $(sq),$(sq)$(backslash)$(sq)$(sq),$(value $(var)))';)

