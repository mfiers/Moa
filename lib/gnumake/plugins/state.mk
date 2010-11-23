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

MOA_INCLUDE_PLUGIN_STATE= yes

moa_targets += state
state_help += shows the current state of this anaolysis

moa_state_insets += $(moa_id)_input_files
moa_state_outsets += $(moa_id)_output_files

.PHONY: state
state: $(addprefix moa_state_,$(moa_state_outsets)) \
	$(addprefix moa_state_,$(moa_state_insets))


define state_target
$(warning creating_state_$(1) : $(1))
$(warning test $(1))
moa_state_$(1): $$($(1))
	$e echo $($(1))
	$e echo x $(1): $$? $$^ y
endef 

$(foreach st,$(moa_state_insets),$(eval $(call state_target,$(st))))
$(foreach st,$(moa_state_outsets),$(eval $(call state_target,$(st))))


