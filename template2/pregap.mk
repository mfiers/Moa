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
clean_help = Clean up.

# Help
moa_id = pregap
template_title = Pregap
template_description = Run Pregap. Note that running phrap could be a part of this. 

# Output definition
moa_outputs += pregap
moa_output_pregap = ./BACS/pregap.output
moa_output_pregap_help = Set of processed BACs

#varables that NEED to be defined
moa_must_define += input_dir
input_dir_help = Directory with the input data
input_dir_type = string

moa_must_define += input_pattern
input_pattern_help = file name pattern
input_pattern_type = string

#moa_must_define += vector_primer
#vector_primer_help = file containt vector primer data

moa_must_define += cloning_vector
cloning_vector_help = File containing the cloning vector
cloning_vector_type = file

moa_must_define += sequencing_vector
sequencing_vector_help = File containing the sequencing vector
sequencing_vector_type = file

moa_must_define += ecoli_screenseq
ecoli_screenseq_help = File containing ecoli screen sequences
ecoli_screenseq_type = file

moa_must_define += repeat_masker_lib
repeat_masker_lib_help = File with a repeatmasker library
repeat_masker_lib_type = file

moa_must_define += vector_primerfile
vector_primerfile_help = File with the vector primers
vector_primerfile_type = file

moa_may_define += quality_value_clip
quality_value_clip_help = quality cutoff
quality_value_clip_type = integer
quality_value_clip_default = 10

moa_may_define += pregap_template
pregap_template_help = the template pregap config file to use. if \
  not defined, Moa tries ./files/pregap.config.
pregap_template_type = file
pregap_template_default = ./files/pregap.config.

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
