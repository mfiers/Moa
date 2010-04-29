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
####  filesets - predefined utilities to handle sets of files
#
################################################################################

moa_fileset_define = \
	$(eval moa_must_define += $(1)_dir) \
	$(eval moa_may_define += $(1)_extension) \
	$(eval moa_may_define += $(1)_glob) \
	$(eval moa_may_define += $(1)_sort) \
	$(eval moa_may_define += $(1)_limit) \
	$(eval $(1)_dir_help = $(3)) \
	$(eval $(1)_dir_type = directory) \
	$(eval $(1)_extension_help = file extension for the files in $(1)_dir) \
	$(eval $(1)_extension_type = string) \
	$(eval $(1)_extension_default = $(2)) \
	$(eval $(1)_glob_help = glob to select a subset of files from $(1)_dir) \
	$(eval $(1)_glob_type = string) \
	$(eval $(1)_glob_default=*) \
	$(eval $(1)_sort_help=Sort order. Choose from: u - unsorted, s - size, \
		sr - size reverse, t - time, tr - time reverse ) \
	$(eval $(1)_sort_type=set) \
	$(eval $(1)_sort_default=u) \
	$(eval $(1)_sort_allowed=u s sr t tr) \
	$(eval $(1)_limit_help=Number of files to use, if not defined: all files) \
	$(eval $(1)_limit_default=) \
	$(eval $(1)_limit_type=integer) \
	$(eval _moa_filesets += $(1))


## functions to remap filesets
## usage: $(call moa_fileset_remap,INPUT_FILESET_ID,OUTPUT_FILESET_ID,OUTPUT_FILETYPE)
moa_fileset_remap = \
	$(eval $(2)_files=\
		$(addprefix $(3)/,$(patsubst %.$($(1)_extension),%.$(3),$(notdir $($(1)_files)))))

moa_fileset_remap_nodir = \
	$(eval $(2)_files=$(patsubst %.$($(1)_extension),%.$(3),$(notdir $($(1)_files))))

