SHELL := /bin/bash
.PHONY: set show help check prereqs

#see if a local variable set is defined
-include moa.mk

moa_targets += check help show all clean_all prereqs
check_help = Check variable definition
show_help = show defined variables
help_help = This help!
all_help = Recursively run through all subdirectories (use make all \
	action=XXX to run "make XXX" recursively) 
prereqs_help = Check if all prerequisites are present


###########################################################################
#check prerequisites
prereqlist += moa_envsettings
.PHONY: prereqs
prereqs: $(prereqlist)

#check if MOABASE is defined
moa_envsettings:
	@if env | grep -q MOABASE ; then true; else \
		echo "MOABASE is not defined :(" ; \
		false ;\
	fi

check: prereqs $(addprefix checkvar_, $(moa_must_define))
	@echo "Variable check: everything appears ok"
	
checkvar_%:
	@if [ "$(origin $(subst checkvar_,,$@))" == "undefined" ]; then \
		echo " *** Error $(subst checkvar_,,$@) is undefined" ;\
		exit -1; \
	fi

wset: $(addprefix storeweka_, $(moa_must_define) $(moa_may_define))

storeweka_%:		 
	@if [ "$(origin $(subst storeweka_,,$@))" == "command line" ]; then \
		echo " *** Set Weka var $(subst storeweka_,,$@) to 'weka get $($(subst storeweka_,,$@))'" ;\
		echo -n "$(subst storeweka_,,$@)=$$" >> moa.mk ;\
		echo "(shell weka get $($(subst storeweka_,,$@)))" >> moa.mk ; \
	fi

set: $(addprefix storevar_, $(moa_must_define) $(moa_may_define))

storevar_%:		 
	@if [ "$(origin $(subst storevar_,,$@))" == "command line" ]; then \
		echo " *** Set $(subst storevar_,,$@) to $($(subst storevar_,,$@))" ;\
		echo "$(subst storevar_,,$@)=$($(subst storevar_,,$@))" >> moa.mk ;\
	fi	
		
show: $(addprefix showvar_, $(moa_must_define) $(moa_may_define))

showvar_%:		 
	@echo "$(subst showvar_,,$@) : $($(subst showvar_,,$@))"

#dir traversing
moa_followups ?= $(shell find . -maxdepth 1 -type d -regex "\..+" -exec basename '{}' \; | sort )

.PHONY: $(moa_followups) all clean_all

all_check:
	@echo "would run make $(action)"
	@echo "in the following dirs"
	@echo $(moa_followups)
	
action ?= all
all: $(moa_followups)
	if [ "$(action)" == "all" ]; then \
		echo "running all without action, also run default action" ;\
		$(MAKE) ;\
	fi
	@echo "follows" $(moa_followups)

$(moa_followups):
	@echo "  ###########################"
	@echo "  ## Executing make $(action)"
	@echo "  ##   in $@ " 
	@echo "  ###########################"
	if [ -e $@/Makefile ]; then \
		cd $@ && $(MAKE) $(action) ;\
	fi

###############################################################################
# Help structure
help: moa_help_header \
	moa_help_target_header moa_help_target moa_help_target_footer \
	moa_help_vars_header moa_help_vars moa_help_vars_footer \
	moa_help_output_header moa_help_output moa_help_output_footer
	
moa_help_header:
	@echo -n "=="
	@echo -n "$(moa_title)" | sed "s/./=/g"
	@echo "=="
	@echo "= $(moa_title) ="
	@echo -n "=="
	@echo -n "$(moa_title)" | sed "s/./=/g"
	@echo "=="
	@echo 
	@echo "$(moa_description)" | fold -s
	@echo

## Help - output section
moa_help_output_header:
	@echo "Outputs"
	@echo "======="

moa_help_output: $(addprefix moa_output_, $(moa_outputs))

moa_output_%:
	@echo -n " - $($@)"
	@if [ "$(origin $@_help)" == "undefined" ]; then \
		echo ;\
	else \
		echo " : $($(subst helpvar_,,$@)_help)"  | fold -s ;\
	fi
	
	
moa_help_output_footer:
	@echo 
	
## Help - target section
moa_help_target_header:
	@echo "Targets"
	@echo "======="

moa_help_target: $(addprefix moa_target_, $(moa_targets))
	
	
moa_target_%:
	@echo -n " - $(subst moa_target_,,$@)"
	@if [ "$(origin $(subst moa_target_,,$@)_help)" == "undefined" ]; then \
		echo ;\
	else \
		echo " : $($(subst moa_target_,,$@)_help)" | fold -s  ;\
	fi
	
	
moa_help_target_footer:
	@echo 

## Help - output section
help_output_header:
	@echo "Output"
	@echo "======"
	
help_output_footer:
	@echo 
	
## Help - variable section
moa_help_vars_header:
	@echo "Variables"
	@echo "========="
	
moa_help_vars_footer:
	@echo "  * these vars must be defined"
	@echo 
	
moa_help_vars: moa_help_vars_must moa_help_vars_may

moa_help_vars_must: help_prefix="*"
moa_help_vars_must: $(addprefix helpvar_, $(moa_must_define))

moa_help_vars_may: help_prefix=" "
moa_help_vars_may: $(addprefix helpvar_, $(moa_may_define))


helpvar_%:
	@echo -n " - $(subst helpvar_,,$@)$(help_prefix)"
	@if [ "$(origin $(subst helpvar_,,$@)_help)" == "undefined" ]; then \
		echo ;\
	else \
		echo " - $($(subst helpvar_,,$@)_help)"  | fold -s;\
	fi
		
		