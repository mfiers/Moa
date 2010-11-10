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
# You should have received a copy	 of the GNU General Public License
# along with Moa.  If not, see <http://www.gnu.org/licenses/>.
# 
include $(MOABASE)/lib/gnumake/prepare.mk

moa_id = bartab

#########################################################################
# Prerequisite testing

#########################################################################
## variable definition

#include the moa core libraries
include $(MOABASE)/lib/gnumake/core.mk
.PHONY: bartab_prepare
bartab_prepare:

.PHONY: bartab_post
bartab_post:

.PHONY: bartab_initialize
bartab_initialize:

.PHONY: bartab_clean
bartab_clean:
	rm bartab.*

.PHONY: bartab
bartab:
	$e bartab -v -in $(bartab_in) \
		$(if $(bartab_qin), -qin $(bartab_qin)) \
		$(if $(bartab_map), -map $(bartab_map)) \
		$(if $(bartab_out), -out $(bartab_out)) \
		$(if $(bartab_forward_primer), -for $(bartab_forward_primer)) \
		$(if $(bartab_reverse_primer), -rev $(bartab_reverse_primer)) \
		$(if $(bartab_min_length), -min $(bartab_min_length)) \
		$(if $(call seq,$(bartab_trim),F),-xbar) \
		$(bartab_extra_parameters) \
		> bartab.out

