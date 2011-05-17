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
moa_id = scaffolder

#variables

include $(MOABASE)/lib/gnumake/core.mk
##### Derived variables for this run

.PHONY: scaffolder_prepare
scaffolder_prepare:

.PHONY: scaffolder_post
scaffolder_post:

.PHONY: scaffolder
scaffolder: $(scaffolder_prefix).png

$(scaffolder_prefix).png: $(scaffolder_input_file) $(scaffolder_reference_file)
	scaffolder $(minv) \
		-i $< -r $(scaffolder_reference_file) -p $(scaffolder_prefix)

scaffolder_clean:
	rm -f $(scaffolder_prefix).*
	rm -f goBambus.*
	rm -f formatdb.log

