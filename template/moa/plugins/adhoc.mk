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

MOA_INCLUDE_PLUGIN_ADHOC = yes

################################################################################
## Git - use git to keep track of project history

.PHONY: moa_plugin_adhoc_test
moa_plugin_adhoc_test:
	moa adhoc -f 'ls -l > output' -t 'test adhoc'
	moa show | grep process | grep -q 'ls'
	moa
	cat output | grep -q 'moa.mk'