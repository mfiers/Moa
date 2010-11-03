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

info: info_header info_targets info_parameters

info_header:
	@echo -e 'moa_id\t$(moa_id)'
	@echo -e 'template_title\t$(template_title)'
	@echo -e 'template_description\t$(template_description)'
	@echo -e 'template_author\t$(template_author)'
	@echo -e 'title\t$(title)'
	@echo -e 'description\t$(description)'
	@echo -e 'moa_files\t$(moa_files)'
	@echo -e 'moa_targets\t$(moa_id) all clean $(moa_additional_targets)'

info_targets: $(addprefix info_target_help_, $(moa_id) all clean $(moa_additional_targets))

info_target_help_%:
	@echo -e "$*_help\t$($*_help)"


info_parameters: info_parameters_required info_parameters_optional

info_parameters_required: mandatory=yes
info_parameters_required: $(addprefix info_par_,$(moa_must_define))

info_parameters_optional: mandatory=no
info_parameters_optional: $(addprefix info_par_,$(moa_may_define))

_mpv=$(subst $(sq),$(sq)$(backslash)$(sq)$(sq),$(value $(1)))
info_par_%:
	@echo -en 'parameter'
	@echo -en '\tname=$*'
	@echo -en '\tmandatory=$(mandatory)'
	@echo -en '\ttype=$*'
	@echo -en '\tvalue='
	@echo -n '$(call _mpv,$*)'
	@echo -en '\tdefault='
	@echo -n '$(call _mpv,$*_default)'
	@echo -en '\tallowed=$($*_allowed)'
	@echo -en '\ttype=$($*_type)'
	@echo -en '\tcardinality=$(if $($*_cardinality),$($*_cardinality),one)'
	@echo -en '\tcategory=$($*_category)'
	@echo -en '\thelp=$($*_help)'
	@echo


.PHONY: moa_plugin_info_test
moa_plugin_info_test:
	x=`moa info` ;\
		(echo $$x | grep -q 'moa_id' ) || \
			($(call exer,moa info does not contain moa_id)); \
		(echo $$x | grep - q'template_title') || \
			($(call exer,moa info does not contain template_title)); \
		(echo $$x | grep -q 'template_description') || \
			($(call exer,moa info does not contain template_description)); \
