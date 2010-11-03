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
include $(MOABASE)/lib/gnumake/prepare.mk

moa_id = vpcr

#########################################################################
# Prerequisite testing

#include moabasemoa	
include $(MOABASE)/lib/gnumake/core.mk
real_vpcr_db = $(if $(vpcr_db), $(shell echo "$(vpcr_db)" | sed "s/\.[pn]..$$//"))

ifdef real_vpcr_db
single_vpcr_db_file=$(shell ls $(real_vpcr_db)*.[pn]s[dq] 2>/dev/null || true)
endif

#echo Main target for vpcr
.PHONY: vpcr
vpcr: vpcr.bowtie.out

vpcr.bowtie.out:
	bowtie --all -l `expr length "$(vpcr_primer_1)"`						\
		-n 2 -c --fr -I $(vpcr_insert_min) -X $(vpcr_insert_max)	\
		 $(vpcr_bowtie_db) -1 $(vpcr_primer_1) -2 $(vpcr_primer_2)	\
			> vpcr.bowtie.out

vpcr_clean:
