# run pregap!

# Main target - should be first in the file
moa_main_target: check pregap


################################################################################
# Definitions
# targets that the enduser might want to use
moa_targets += pregap clean
pregap_help = Run pregap
clean_help = Clean up. 

# Help
moa_ids += pregap
moa_title_pregap = Pregap
moa_description_pregap = Run Pregap. Note that running phrap could be a part of this. 

# Output definition
moa_outputs += pregap
moa_output_pregap = ./BACS/pregap.output
moa_output_pregap_help = Set of processed BACs

#varables that NEED to be defined
moa_must_define += input_dir
input_dir_help = Directory with the input data

moa_must_define += input_pattern
input_pattern_help = file name pattern

#moa_must_define += vector_primer
#vector_primer_help = file containt vector primer data

moa_must_define += cloning_vector
cloning_vector_help = File containing the cloning vector
 
moa_must_define += sequencing_vector
sequencing_vector_help = File containing the sequencing vector

moa_must_define += ecoli_screenseq
ecoli_screenseq_help = File containing ecoli screen sequences

moa_must_define += repeat_masker_lib
repeat_masker_lib_help = File with a repeatmasker library

moa_may_define += quality_value_clip
quality_value_clip_help = quality cutoff


#Include base moa code - does variable checks & generates help
ifndef dont_include_moabase
	include $(shell echo $$MOABASE)/template/moaBase.mk
endif

################################################################################

.PHONY: pregap
pregap: pregap_start pregap_run

.PHONY: pregap_start
pregap_start:
	
.PHONY: pregap_run
pregap_touchfiles = $(addsuffix /touched, $(notdir $(shell find $(input_dir) -name "$(input_pattern)" -type d)))
pregap_run: $(pregap_touchfiles)

$(pregap_touchfiles): %/touched : $(realpath $(input_dir))/%
	@echo processing $@ from $<
	-mkdir $(subst /touched,,$@)	
	#create a fof	
	cd $(subst /touched,,$@); find $< -name '*.ab?' > $(subst /touched,,$@).fof	
	#create the pregap config file	
	cat $(pregap_template) \
        | sed "s|PROJECTNAME|$(subst /touched,,$@)|" \
        | sed "s|ECOLISCREENSEQFILE|$(ecoli_screenseq)|" \
        | sed "s|REPEATMASKERLIB|$(repeat_masker_lib)|" \
        | sed "s|CLONINGVECTORFILE|$(cloning_vector)|" \
        | sed "s|QUALCLIPVALUE|$(quality_value_clip)|" \
        | sed "s|SEQUENCINGVECTORFILE|$(sequencing_vector)|" \
        > ./$(subst /touched,,$@)/pregap.conf
    #move in the dir & execute pregap4
	cd $(subst /touched,,$@) ;\
			pregap4 -nowin -config pregap.conf -fofn $(subst /touched,,$@).fof > pregap.report 2> pregap.err
	#
	#see if there is a phasefile, if not. create one.
	sqid=$(subst /touched,,$@) ;\
		for phph in $$sqid/$$sqid.?.phase; do \
			if [ ! -f $$phph ] ; then \
				echo "1" > $$phph ;\				
			fi ;\
		done
	#		
	#create a touchfile - prevent reexecution
	touch $(subst /touched,,$@)/touched		

#CLEAN	    
.PHONY: clean    
clean: pregap_clean

.PHONY: pregap_clean
pregap_clean:
	@echo "TODO: Run clean"
		