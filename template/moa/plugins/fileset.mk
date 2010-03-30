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


## Evaluate & load the filesets

ifdef $(moa_id)_main_phase
$(foreach v,$(_moa_filesets), \
	$(eval $(v)_srtst=cat) \
	$(eval $(v)_realext=$(if $($(v)_extension),.$(v)_extension)) \
	$(if $(call seq,$($(v)_sort),u), \
		$(eval $(v)_prtst=%A@)) \
	$(if $(call seq,$($(v)_sort),t), \
		$(eval $(v)_srtst=sort -n)$(eval $(v)_prtst=%A@)) \
	$(if $(call seq,$($(v)_sort),tr), \
		$(eval $(v)_srtst=sort -nr)$(eval $(v)_prtst=%A@)) \
	$(if $(call seq,$($(v)_sort),s), \
		$(eval $(v)_srtst=sort -n)$(eval $(v)_prtst=%s)) \
	$(if $(call seq,$($(v)_sort),sr), \
		$(eval $(v)_srtst=sort -nr)$(eval $(v)_prtst=%s)) \
	$(if $($(v)_limit),$(eval $(v)_lmtst=|head -n $($(v)_limit))) \
	$(eval $(v)_files=$(shell \
				find $($(v)_dir)/ -maxdepth 1 \
					-name '$($(v)_glob)$($(v)_realext)' \
					-printf '$($(v)_prtst)\t%p\n' \
			| ( $($(v)_srtst) 2>/dev/null ) \
			$($(v)_lmtst) \
			| cut -f 2 )))
endif

moa_fileset_init = $(warning use of moa_fileset_init is deprecated)
