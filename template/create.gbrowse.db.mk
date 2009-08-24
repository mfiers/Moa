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
moa_title = Initalize GBrowse
moa_description = Initalizes a GBrowse database, including some			\
  additional features (extra columns & tables used by other software    \
  developed by the author)
gup_gffsource = Not used, this is a dummy

include $(shell echo $$MOABASE)/template/__upload2gbrowse.mk

#override the default goal.
.DEFAULT_GOAL := runInitGbrowse

#remove gup_gff_source from the list of MUST defines
runInitGbrowse: blabla moa_prepare_var moa_check moa_preprocess initGbrowse

blabla:
	@echo $(moa_must_define)