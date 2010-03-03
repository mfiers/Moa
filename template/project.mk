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
moa_title = Project
moa_description = Create a new project. All subdirectories of this directory are automatically a part of this project

moa_ids += project
project_help = This template does not do anything - it is a project placeholder.

moa_may_define += project_description
project_description_default = 
project_description_help = A description of what this project is				\
  supposed to achieve, how to use it, and what parameters are most				\
  important to set
project_description_type = string

#include moabase, if it isn't already done yet..
include $(shell echo $$MOABASE)/template/moaBase.mk

.PHONY: project_initialize
project_initialize:
	-mkdir moa

.PHONY: project_clean
project_clean:

.PHONY: project_prepare
project_prepare:

.PHONY: project_post
project_post:

.PHONY: project
project:

