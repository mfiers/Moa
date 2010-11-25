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
moa_id = bowtiedb

#########################################################################
# Prerequisite testing

#variables

test2:
	@echo $(bowtiedb_input_files)
	@echo $(call merge,b, a a a )

include $(MOABASE)/lib/gnumake/core.mk
bowtiedb: $(bowtiedb_name).1.ebwt

#one of the database files
comma=,
$(bowtiedb_name).1.ebwt: $(bowtiedb_input_files)
	-$e rm -f $(bowtiedb_name).*.ebwt
	echo bowtie-build $(call merge,$(comma),$^) $(bowtiedb_name)
	$e bowtie-build $(call merge,$(comma),$^) $(bowtiedb_name)
	touch $(bowtiedb_name)

bowtiedb_clean:
	-rm -f $(bowtiedb_name).*.ebwt

