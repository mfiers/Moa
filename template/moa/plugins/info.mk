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
## make info ###################################################################
#
#### Show lots of information on the current job
#
################################################################################

info_keyval = "$(1)" : "$(subst '"',"'",$(2))"
info_keyvallist = "$(1)" : [$(call merge,$(comma),$(foreach v,$(2),"$(subst '"',"'",$(v))"))]

.PHONY: info info_header info_parameters info_parameters_optional	\
		info_parameters_required

info: info_header info_parameters

info_header:
	@echo -e 'moa_title\t$(moa_title)'
	@echo -e 'moa_description\t$(moa_description)'
	@echo -e 'moa_targets\t$(moa_id) all clean $(moa_additional_targets)'

info_parameters: info_parameters_required info_parameters_optional

info_parameters_required: mandatory=yes
info_parameters_required: $(addprefix info_par_,$(moa_must_define))

info_parameters_optional: mandatory=no
info_parameters_optional: $(addprefix info_par_,$(moa_may_define))

info_par_%:
	@echo -en 'parameter'
	@echo -en '\tname=$*'
	@echo -en '\tmandatory=$(mandatory)'
	@echo -en '\ttype=$*'
	@echo -en '\tvalue=$($*)'
	@echo -en '\tdefault=$($*_default)'
	@echo -en '\tallowed=$($*_allowed)'
	@echo -en '\ttype=$($*_type)'
	@echo -en '\tcardinality=$(if $($*_cardinality),$($*_cardinality),one)'
	@echo -en '\tcategory=$($*_category)'
	@echo -en '\thelp=$($*_help)'
	@echo

