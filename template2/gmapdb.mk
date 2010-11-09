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
moa_id = gmapdb

#variables

ifndef dont_include_moabase
	include $(shell echo $$MOABASE)/template/moa/core.mk
endif

##### Derived variables for this run
moa_register_extra += gmapdb
moa_register_gmapdb = $(shell echo `pwd`)/$(gmapdb_name)

gmapdb_input_files = $(wildcard $(gmapdb_input_dir)/*.$(gmapdb_input_extension))

.PHONY: gmapdb_prepare
gmapdb_prepare:
	@echo "--" $(gmapdb_input_files)

.PHONY: gmapdb_post
gmapdb_post:

.PHONY: gmapdb
gmapdb: Makefile.$(gmapdb_name)
	$(MAKE) -f $< coords
	$(MAKE) -f $< gmapdb
	touch $(gmapdb_name)

Makefile.$(gmapdb_name):
	gmap_setup -S -d $(gmapdb_name) $(gmapdb_input_files)

gmapdb_clean:
	rm -f $(gmapdb_name).*
	rm -f coords.$(gmapdb_name)
	rm -f Makefile.$(gmapdb_name)
	rm -f INSTALL*

