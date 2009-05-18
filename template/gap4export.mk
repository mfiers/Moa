# export data from an assembly using gap4!

# Main target - should be first in the file
moa_main_target: check gap4export


################################################################################
# Definitions
# targets that the enduser might want to use
moa_targets += gap4export clean
gap4export_help = Export data from an assembly using gap4
clean_help = Clean up. 

# Help
moa_ids += gap4export
moa_title_gap4export = Assembly export using gap4
moa_description_gap4export = Export data from an assembly using gap4

# Output definition
moa_outputs += g4ephase
moa_output_g4ephase = ./BACID.phase
moa_output_g4ephase_help = phase of the BAC (1-3)

#varables that NEED to be defined
moa_must_define += input_dir
input_dir_help = Directory with the input data

moa_must_define += input_pattern
input_pattern_help = file name pattern

#Include base moa code - does variable checks & generates help
ifndef dont_include_moabase
	include $(shell echo $$MOABASE)/template/moaBase.mk
endif

################################################################################

.PHONY: gap4export
gap4export: gap4export_run


infiles = $(notdir $(shell find $(input_dir) -name "$(input_pattern)" -type d))
gap4export_phase = $(addprefix .phase, $(infiles))

.PHONY: gap4export_run
gap4export_run: $(gap4export_phase)

$(gap4export_phase): %.phase : $(realpath $(input_dir))/%
	@echo processing $@ from $<
	#see if there is a phasefile, if not. create one.
	#sqid=$(subst /touched,,$@) ;\
	#		for phph in $$sqid/$$sqid.?.phase; do \
	#		if [ ! -f $$phph ] ; then \
	#			echo "1" > $$phph ;\				
	#		fi ;\
	#	done
		
	#exportContigs.tcl $dbBaseName %(version)s %(id)s
	
#CLEAN	    
.PHONY: clean    
clean: pregap_clean

.PHONY: pregap_clean
pregap_clean:
	@echo "TODO: Run clean"
		