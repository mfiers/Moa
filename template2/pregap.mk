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
moa_main_target: check pregap

################################################################################
# Definitions
# targets that the enduser might want to use
moa_targets += pregap pregap_post clean

# Help
moa_id = pregap

# Output definition
moa_outputs += pregap
moa_output_pregap = ./BACS/pregap.output

#varables that NEED to be defined

#Include base moa code - does variable checks & generates help
ifndef dont_include_moabase
	include $(shell echo $$MOABASE)/template/moa/core.mk
endif

quality_value_clip ?= 10

.PHONY: pregap_prepare
pregap_prepare:

.PHONY: pregap_post
pregap_post:

.PHONY: pregap
pregap_touchfiles = $(addsuffix /touched, \
		$(notdir $(shell find $(input_dir) \
		-name "$(input_pattern)" -type d)))
pregap: $(pregap_touchfiles)

$(pregap_touchfiles): %/touched : $(realpath $(input_dir))/%
	@echo processing $@ from $<
	-mkdir $(subst /touched,,$@)	
	@#create a fof	
	cd $(subst /touched,,$@); find $< -name '*.ab?' > $(subst /touched,,$@).fof	
	@#create the pregap config file	
	cat $(pregap_template) \
        | sed "s|PROJECTNAME|$(subst /touched,,$@)|" \
        | sed "s|VECTORPRIMERFILE|$(vector_primerfile)|" \
        | sed "s|ECOLISCREENSEQFILE|$(ecoli_screenseq)|" \
        | sed "s|REPEATMASKERLIB|$(repeat_masker_lib)|" \
        | sed "s|CLONINGVECTORFILE|$(cloning_vector)|" \
        | sed "s|QUALCLIPVALUE|$(quality_value_clip)|" \
        | sed "s|SEQUENCINGVECTORFILE|$(sequencing_vector)|" \
        > ./$(subst /touched,,$@)/pregap.conf
    #move in the dir & execute pregap4
	cd $(subst /touched,,$@) ;\
			pregap4 -nowin -config pregap.conf \
					-fofn $(subst /touched,,$@).fof \
				> pregap.report \
				2> pregap.err
	@#create a touchfile - prevent reexecution
	touch $(subst /touched,,$@)/touched

#CLEAN	    
.PHONY: clean    
clean: pregap_clean

.PHONY: pregap_clean
pregap_clean:
	@echo "TODO: Run clean"
